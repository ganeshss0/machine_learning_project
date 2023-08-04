from flask import Flask, request, jsonify

app = Flask(__name__)



@app.route('/', methods=['POST', 'GET'])
def homepage():
    return 'This page is running'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)