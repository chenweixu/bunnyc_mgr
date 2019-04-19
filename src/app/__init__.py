from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db_url = app.config['BUNNYC_MYSQL_URL']
db_user = app.config['BUNNYC_MYSQL_USER']
db_pw = app.config['BUNNYC_MYSQL_PW']
db_name = app.config['BUNNYC_MYSQL_DB']

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_pw}@{db_url}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

# from app.views import apiv1
from app.views import apiv2
# from app.views import apitest
