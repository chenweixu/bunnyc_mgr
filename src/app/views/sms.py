
from app import app
from flask import request
from flask import jsonify

from app.utils.mylog import My_log
from app.main.conf import conf_data
from app.main.sms_tools import Sms_tools


logfile = conf_data("work_log")
log_evel = conf_data("log_evel")
work_log = My_log(logfile, log_evel).get_log()

@app.route('/api/v2/sms', methods=['GET', 'POST'])
def sms_send():
    if request.method == 'GET':
        work_log.debug(str(request.path))

        phone = request.args.get('phone')
        if not phone:
            return 'error', 404
        else:
            body = request.args.get('body')
            work_log.info(str(body))

            phone_list = phone.split(',')
            work_log.debug(str(phone_list))

            sms = Sms_tools()

            data = sms.send_mess(phone_list, body)
            if data == 1:
                work_log.error('link sms webservice interface error')
                return '', 510
            elif data == 2:
                work_log.error('webservice interface args error')
                return '', 511
            else:
                work_log.debug(str('sms_send yes-------------'))
                return '', 200
    else:
        return 'error', 404
