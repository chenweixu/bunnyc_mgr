import json
from app import app
from flask import request
from flask import jsonify
from app.utils.myencrypt import create_key, verify_key
from app.main.cmdb import cmdb
from app.main.conf import conf_data
from app.utils.mylog import My_log

logfile = conf_data("work_log")
log_evel = conf_data("log_evel")
work_log = My_log(logfile, log_evel).get_log()


@app.route('/api/v2/cmdb/<unit>', methods=['GET', 'POST'])
def cmdbInfo(unit):
    if request.method == "POST":
        try:
            key = request.json.get("key")
            if verify_key(key) and request.json.get("obj") == 'cmdb':
                info = cmdb()
                data = info.run_task(request.json.get('content'))
                return jsonify(data)
            else:
                work_log.error("req verify_key or obj error")
                return "", 404
        except Exception as e:
            work_log.error('req cmdb error')
            work_log.error(str(e))
            return str(e), 500
