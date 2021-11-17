import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import csv
from bs4 import BeautifulSoup
import json
import traceback
import subprocess
import os.path
from subprocess import Popen, PIPE, STDOUT


def main():
    data = []
    # header = ['url', 'monthly visits', 'category', 'visit1', 'visit2', 'visit3', 'visit4', 'visit5',
    #           'top referring site']
    header = ['url', 'monthly visits', 'visit0', 'visit1', 'visit2', 'visit3', 'visit4', 'visit5']
    visit = ''
    category = ''
    count = 0
    top_referring_sites = ''
    for cmp in companies:
        count = count +1
        print(count)
        print(cmp)
        url = "https://web.vstat.info/{}".format(cmp)
        visits_list = ['N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A']
        tmp = []
        try:
            driver.get(url)
            time.sleep(2)
            visit = driver.find_element_by_xpath("//span[@class='time-dot-sum']").text.strip()
            # category = driver.find_element_by_xpath("//div[@class='category-choise']").text.strip()
            try:
                r = requests.get(url)
                bs = BeautifulSoup(r.text, "html.parser")
                scripts = bs.find_all('script')
                if len(scripts) > 0:
                    vscr = scripts[5]
                    if 'json_graphic' in vscr.text:
                        main_script = vscr.text
                        script = main_script.split('var json_graphic= ')[1]
                        visits = script.split(';')[0]
                        visits_json = json.loads(visits)
                        if visits_json:
                            visits_list = [*visits_json.values()]

                # for s in scripts:
                #     if 'json_graphic' in s.text:
                #         main_script = s.text
                #         script = main_script.split('var json_graphic= ')[1]
                #         print("sss {}".format(script))
                #         visits = script.split(';')[0]
                #         visits_json = json.loads(visits)
                #         if visits_json:
                #             visits_list = [*visits_json.values()]
                        # script1 = main_script.split(";")[0]
                        # top_referring_sites = script1.split("var json_refferals= ")[1]
                # tmp = [cmp, visit, category, str(top_referring_sites)[1:-1].replace(",","\n\r").replace('"','')]
                tmp = [cmp, visit]
                final = tmp[:2] + visits_list[0:6] + tmp[2:]
                data.append(final)
            except Exception:
                print("exception inside")
                tmp = [cmp, visit]
                final = tmp[:2] + visits_list[0:6] + tmp[2:]
                data.append(final)
                traceback.format_exc()
        except Exception:
            print("exception outside")
            tmp = [cmp, "N/A", "N/A", 'N/A']
            final = tmp[:2] + visits_list[0:6] + tmp[2:]
            data.append(final)
            traceback.format_exc()

    with open('upwork_new_2500.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write multiple rows
        writer.writerows(data)

    driver.close()
    # print("CSV generation successful")
    # cmd = "aws s3 cp upwork_new_2500.csv s3://om-sqs/OM/om_qc/processingDashboard/scrub/scripts/test/test.csv"
    # subprocess.call(cmd, shell=True)

if __name__ == '__main__':
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options, executable_path="/Users/uttam.sapkota/Downloads/chromedriver")
    df = pd.read_csv("/Users/uttam.sapkota/Downloads/domains.csv")

    companies = df["domain"].tolist()
    # companies = ['oldtimepottery.com']
    main()
