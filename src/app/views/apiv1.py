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


@app.route('/api/v1/sms/send', methods=['GET', 'POST'])
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


@app.route('/api/v1/showsysteminfo', methods=['POST'])
def HostManagerShowSyetemInfo():
    try:
        des_ip = request.json.get('des_ip')
        task = request.json.get('task')
    except Exception as e:
        work_log.error('req args error')
        work_log.debug(str(e))
        return '', 501

    work_log.info('request showsysteminfo, ip: %s' % (request.remote_addr))
    work_log.info('des_ip: %s, task: %s' % (des_ip, task))

    info = HostBaseCmd(des_ip)
    data = info.runtask(task=task)
    return jsonify(data)


@app.route('/api/v1/hostcmd', methods=['POST'])
def HostManagerhostcmd():
    cmd = request.json.get('cmd')
    des_ip = request.json.get('des_ip')
    user = request.json.get('user')
    work_log.info('request ip: %s' % (request.remote_addr))
    work_log.info('user: %s, des_ip: %s, cmd: %s' % (user, des_ip, cmd))
    default_user = conf_data.get('user_info', "default_user")
    if user != default_user:
        return 'req format error', 403

    info = HostBaseCmd(des_ip)
    data = info.runtask(cmd=cmd)
    return jsonify(data)


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


@app.route('/api/v1/weblogic', methods=['GET'])
def ServiceManagerWeblogic():
    work_log.info('---------------- weblogic start ---------------')
    work_log.info('request hosts: ' + request.remote_addr)
    task = request.args.get('task')
    work_log.info(task)
    info = WeblogicManager()
    if task == 'start_group' or task == 'stop_group':
        group_number = request.args.get('group_number')
        work_log.debug(group_number)
        data = info.run_task_group(task, group_number)
    elif task in ('start', 'stop', 'show_access_log', 'show_error_log'):
        service_number = request.args.get('service_number')
        hosts = request.args.get('hosts')
        work_log.debug(service_number)
        data = info.run_task(hosts, task, service_number)
    else:
        data = {'recode': 9, 'redata': '参数错误'}
    work_log.info(data)
    work_log.info('---------------- weblogic end ----------------')
    return jsonify(data)


@app.route('/api/v1/nginx', methods=['POST'])
def service_mgr_nginx():
    work_log.info('service_mgr_nginx')
    task = request.json.get('task')
    lock_ip = request.json.get('lock_ip')
    webserver = request.json.get('webserver')
    try:
        if task in ['lock', 'ulock', 'showlock']:
            work_log.info(
                'nginx task: %s :  ip: %s' % (str(task), str(lock_ip)))
            info = NginxManager()
            data = info.lock_ip(lock_ip, task)
            return jsonify(data)

        elif webserver:
            work_log.debug('request nginx, webserver: ' + str(webserver) +
                           ' task: ' + str(task))
            info = NginxManager()
            data = info.nginx_task(webserver, task)
            return jsonify(data)
        else:
            work_log.error('recode: 9999, req format error')
            return jsonify({'recode': 9999, 'data': 'req format error'})
    except Exception as e:
        work_log.error('task run error')
        work_log.error(str(e))
        return jsonify({'recode': 999, 'data': 'task run error'})


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


@app.route('/api/v1/memcached', methods=['POST'])
def memcached():
    work_log.info(str(request.json))
    work_log.info(str(request.path))

    try:
        info = MemcachedManager()
        if request.json.get('task') in ['start', 'stop', 'reboot']:
            data = info.run_task(request.json)
            work_log.info('return data: ' + str(data))
            return jsonify(data)
        elif request.json.get('task') in [
                'link_sum', 'get', 'set', 'cleardata'
        ]:
            data = info.data_task(request.json)
            work_log.info('return data: ' + str(data))
            return jsonify(data)
        else:
            return jsonify({"recode": 99, "redata": 'format error'})
    except Exception as e:
        work_log.error('api memcached error')
        work_log.error(str(e))
        return jsonify({"recode": 9, "redata": 'api error'})
