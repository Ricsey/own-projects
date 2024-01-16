import requests
import json
from flask import render_template, url_for, jsonify
from app.utils.random_generator import dummy_table, dummy_sinnach_table, dummy_error_types
from app import app

@app.route('/')
@app.route('/summary')
def summary():
    return render_template('summary.html', table=dummy_table)


@app.route("/sinnach", methods=["POST", "GET"])
def sinnach():
    #return jsonify(dummy_sinnach_table)
    #requests.post('http://localhost:5000/sinnach', data=json.dumps(dummy_sinnach_table)) 
    return render_template('sinnach.html', runs_table = dummy_sinnach_table, runs=dummy_error_types)

@app.route("/testcase")
def testcase():
    return render_template('testcase.html')