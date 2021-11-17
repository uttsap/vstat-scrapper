from flask import Flask, request, jsonify
import json
app = Flask(__name__)

# Flask maps HTTP requests to Python functions.
# The process of mapping URLs to functions is called routing.
@app.route('/', methods=['GET'])
def home():
    return "<h1>Vstat Callback</h1><p>This is a prototype API</p>"

@app.route('/app/get', methods=['GET'])
def read():
    final_arr = []
    try:
        with open('file.json', 'r') as outfile:
            for obj in outfile:
                a = obj.strip().split("~")

            del a[-1]
            for ele in a:
                js = json.loads(ele)
                final_arr.append(js)
        return jsonify({"stats":final_arr}), 200

    except Exception as e:
        print(e)
        return jsonify({"stats":final_arr}), 500

@app.route('/app/callback' , methods = ['POST'])
def callback():
    if not request.is_json:
        return "<p>The content isn't of type JSON<\p>"
    try:
        content = request.get_json()
        print("Content {}".format(content))
        with open('file.json', 'a') as outfile:
            outfile.write(json.dumps(content))
            outfile.write("~")
            outfile.close()
        return "OK", 200
    except Exception as e:
        print(e)
        print("exception occurred")
        return "Error", 500

# # A method that runs the application server.
# if __name__ == "__main__":
#     # Threaded option to enable multiple instances for multiple user access support
#     app.run(debug=True, threaded=True, port=5000)