from flask import Flask, request, jsonify, render_template
from flask_cors import cross_origin, CORS
app = Flask(__name__)
CORS(app)



@app.route('/', methods=['POST', 'GET'])
@cross_origin()
def homepage() -> str:
    '''Render HomePage'''
    return render_template('report.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)