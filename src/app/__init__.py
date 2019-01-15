from flask import Flask

app = Flask(__name__)

from app.views import apiv1
# from app.views import apitest
