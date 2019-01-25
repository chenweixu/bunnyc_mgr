from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

# from app.views import apiv1
from app.views import apiv2
# from app.views import apitest
