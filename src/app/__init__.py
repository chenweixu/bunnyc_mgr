from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.main.conf import conf_data
from app.utils.mylog import My_log

app = Flask(__name__)

db_url = conf_data('db', 'BUNNYC_MYSQL_URL')
db_user = conf_data('db', 'BUNNYC_MYSQL_USER')
db_pw = conf_data('db', 'BUNNYC_MYSQL_PW')
db_name = conf_data('db', 'BUNNYC_MYSQL_DB')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_pw}@{db_url}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SQLALCHEMY_ECHO'] = True


log_file = conf_data("work_log")
log_level = conf_data("log_level")
work_log = My_log(log_file, log_level).get_log()

db = SQLAlchemy(app)

from app.views import apiv2
from app.views import local
from app.views import host
from app.views import cmdb
from app.views import network
from app.views import nginx_acl
from app.views import monitor
from app.views import sms
from app.views import file
from app.views import service

# from app.views import apitest
