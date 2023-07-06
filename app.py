from flask import Flask, request, Response
from flask_cors import *


app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/', methods=['post', 'get'])
def page():
    return 'here is resume analyse'


@app.route('/api/single/', method=['POST'])
def analyse_single():

    """
        单个简历的识别
        OCR -> 分块 -> txt -> paddlenlp -> json -> return
    :return:
    """

    pass
