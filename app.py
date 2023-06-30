from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/')
def page():
    return 'here is resume analyse'

@app.route('/api/single/', method=['POST'])
def analyse_single():
    pass
