import os
import json
from app import app
from flask import request
from flask import jsonify
from app.utils.myencrypt import create_key, verify_key

from app.main.conf import conf_data
from app.utils.mylog import My_log


logfile = conf_data("work_log")
log_evel = conf_data("log_evel")
work_log = My_log(logfile, log_evel).get_log()
