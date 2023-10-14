from flask import Flask, request, jsonify
from flask_cors import cross_origin, CORS
app = Flask(__name__)
CORS(app)



@app.route('/', methods=['POST', 'GET'])
@cross_origin()
def homepage():
    return 'This page is running'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)