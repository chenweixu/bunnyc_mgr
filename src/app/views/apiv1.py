import json
from app import app
from flask import request
from flask import jsonify
from app.main.mylog import My_log
from app.main.conf import conf_data
from app.main.sms_tools import Sms_tools
from app.main.web import CheckWebInterface
from app.main.memcached import Memcached
from app.main.hostshell import HostBaseCmd
from app.main.servicemanager import NginxManager
from app.main.servicemanager import WeblogicManager
from app.main.servicemanager import MemcachedManager
from app.main.networkmanager import NetworkManager

logfile = conf_data('work_log')
log_evel = conf_data('log_evel')
work_log = My_log(logfile, log_evel).get_log()



@app.route('/api/v1/network', methods=['GET', 'POST'])
def network():
    if request.method == 'GET':
        ipaddr = request.args.get('host')
        work_log.debug('network ping, request ip: ' + request.remote_addr)
        if not ipaddr:
            work_log.error(str('not found ipaddr'))
            return 'error', 404
        else:
            try:
                info = NetworkManager()
                data = info.local_ping(ipaddr)
                work_log.info(str(data))
                return jsonify(data)
            except Exception as e:
                work_log.error('NetworkManager local_ping error')
                work_log.error(str(e))

    elif request.method == 'POST':
        work_log.debug('request ip: ' + request.remote_addr)
        try:
            task = request.json.get('task')
            if len(request.json) < 1 or not task:
                work_log.info(str('data from error'))
                return '', 404
        except Exception as e:
            work_log.error(str('data from error'))
            work_log.error(str(e))
            return '', 404

        if task == 'check_port':
            work_log.info('network check_port, request ip: ' +
                          request.remote_addr)
            work_log.info('network check_port, sip: ' +
                          str(request.json.get('sip')))
            work_log.info('network check_port, ip: ' +
                          str(request.json.get('ip')))
            work_log.info('network check_port, port: ' +
                          str(request.json.get('port')))
            if request.json.get('sip') == '127.0.0.1':
                info = NetworkManager()
                try:
                    recode = info.port_scan(
                        request.json.get('ip'), request.json.get('port'))
                except Exception as e:
                    work_log.error(str(e))
                    recode = '1'
                data = {'recode': recode}
                return jsonify(data)
            else:
                source_ip = request.json.get('sip')
                des_ip = request.json.get('ip')
                des_port = request.json.get('port')

                info = HostBaseCmd(source_ip, scp=True)
                data = info.net_port_scan(ip=des_ip, port=des_port)
                work_log.debug(str(data))
                return jsonify(data)
        elif task == 'iptable':
            return '', 404
        else:
            work_log.debug(str('task not found'))
            return '', 404
    else:
        work_log.info('request.method no get or post')
        return '', 404

@app.route('/api/v1/checkweburl', methods=['GET'])
def ServiceCheckWebUrl():
    # work_log.info(request.path)
    url = request.args.get('url')
    work_log.info('checkweburl: ' + str(url))
    if not url:
        work_log.error('args error')
        return 'args error', 499
    work_log.info(str(url))
    try:
        info = CheckWebInterface()
        recode = info.get_url_status_code(url, timeout=2)
        work_log.debug(str(recode))
        return '', recode
    except Exception as e:
        work_log.error('checkweburl error')
        work_log.error(str(e))
        return 'checkweburl error', 498

