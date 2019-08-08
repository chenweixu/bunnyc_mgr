from app import app
from flask import request
from flask import jsonify
from app.utils.myencrypt import create_key, verify_key
from app.main.conf import conf_data
from app.main.monitor_data import MonitorTask
from app.main.cmdb import cmdb
from app import work_log

@app.route("/")
def index():
    # run_model = app.config['RUN_MODEL']
    data = "Hello cwx!"
    work_log.info(data)
    return str(data), 200



