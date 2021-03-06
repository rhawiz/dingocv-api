import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import *

app = Flask(__name__)
db = SQLAlchemy(app)

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

import jinja2

my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader(['templates']),
])
app.jinja_loader = my_loader

logger = logging.getLogger(__name__)
syslog = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
syslog.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(syslog)
