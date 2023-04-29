from flask import Flask, jsonify
from cloth import *

app  = Flask(__name__)


@app.route('/')
def home():
    
    return

@app.route('/tryon', methods=['POST'])
def tryOn():

    return


if __name__ == '__main__':
    app.run(debug=True, port=4000)