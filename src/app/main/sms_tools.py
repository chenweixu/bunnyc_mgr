# -*- coding: utf-8 -*-
# Email: chenwx716@163.com
# DateTime: 2017-12-01 15:32:37
__author__ = "chenwx"

import hashlib
from suds.client import Client
from app.main.conf import conf_data
from app.main.util.mylog import My_log

logfile = conf_data("work_log")
log_evel = conf_data("log_level")
work_log = My_log(logfile, log_evel).get_log()


class Sms_tools(object):
    """docstring for Sms_tools"""

    def __init__(self):
        super(Sms_tools, self).__init__()

    def md5s(self, body):
        m = hashlib.md5()
        m.update(body.encode("utf8"))
        return m.hexdigest()

    def send_mess(self, mobile_list, content):
        rspXml_body = []

        url = conf_data("sms_conf", "url")
        password = conf_data("sms_conf", "passwd")

        try:
            work_log.info(url)
            work_log.info(mobile_list)
            client = Client(url)
        except Exception as e:
            work_log.error("link sms webservice interface url error")
            work_log.error(str(e))
            return 1

        for mobile in mobile_list:
            reqXml = (
                """<?xml version=\"1.0\" encoding=\"UTF-8\"?> <SmsServiceReq><SmsList>
                <Mobile>"""
                + mobile
                + """</Mobile>
                <Contents><![CDATA["""
                + content
                + """]]></Contents></SmsList>
            </SmsServiceReq>"""
            )
            work_log.debug("-------------------------------------")
            work_log.debug(str(mobile))
            work_log.debug("send sms xml")
            work_log.debug(str(reqXml))
            work_log.debug("-------------------------------------")
            action = "00"
            target = "0101"
            brief = self.md5s(password + action + reqXml + target)
            try:
                rspXml = client.service.smsService(target, action, reqXml, brief)
                work_log.info("send_mess yes-----------------------------")
                work_log.info(str(mobile))
                work_log.info(str(content))
                work_log.info("send_mess rspXml---------------------------")
                work_log.info(str(rspXml))
                work_log.info("send_mess yes-----------------------------")
            except Exception as e:
                work_log.error("send_mess error----------------------------")
                work_log.error(str(reqXml))
                work_log.error("send_mess error----------------------------")
                work_log.error(str(e))
                work_log.error("send_mess error----------------------------")
                return 2
            rspXml_body.append(rspXml)
        return rspXml_body

