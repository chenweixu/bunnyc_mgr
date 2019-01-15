import json
from app import app
from flask import request
from flask import jsonify
from app.main.mylog import My_log
from app.main.conf import conf_data
from app.main.hostshell import HostGroupCmd


logfile = conf_data('work_log')
work_log = My_log(logfile,10).get_log()


@app.route('/api/v1/doc', methods=['GET','POST'])
def DocManager():
    if request.method == 'GET':
        work_log.debug(str(request.path))

        return jsonify(data)
    if request.method == 'POST':
        docid = request.json.get('docid')
        work_log.info('req doc, docid: '+str(docid))

        return jsonify(data)

