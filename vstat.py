import requests
from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
from openpyxl import Workbook
import pandas as pd
import csv
from multiprocessing import Pool
from bs4 import BeautifulSoup
import json
import re
import traceback

api_key = '79cda5ddfb4a97a24f581de8f9409ad8'
def main():
    data = []
    header = ['url', 'monthly visits', 'category', 'visit1', 'visit2', 'visit3', 'visit4', 'visit5',
              'top referring site']
    visit = ''
    category = ''
    count = 0
    top_referring_sites = ''
    for cmp in companies:
        count = count +1
        print(count)
        print(cmp)
        url = "https://web.vstat.info/api.v1.4.php?method=get&apikey={}&url={}".format(api_key, cmp)
        visits_list = ['N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A']
        tmp = []
        try:
            try:
                r = requests.get(url)
                print(r.text)

            except Exception:
                print("exception inside")
        except Exception:
            print("exception outside")
            traceback.format_exc()


if __name__ == '__main__':
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options, executable_path="/Users/uttam.sapkota/Downloads/chromedriver")
    df = pd.read_csv("/Users/uttam.sapkota/Downloads/test.csv")

    companies = df["URL"].tolist()
    # companies = ['vstat.info']
    main()
