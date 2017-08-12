import os

import logging

base_dir = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger(__name__)
syslog = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
syslog.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(syslog)


class Config(object):
    if os.environ.get('DATABASE_URL') is None:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'dingocv.db')
    else:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_MIGRATE_REPO = os.path.join(base_dir, 'db_repository')
    SQLALCHEMY_RECORD_QUERIES = True
    UPLOAD_FOLDER = os.path.join(base_dir, 'app/static/content')
    UPLOAD_URL = '/content'
    STATIC_URL = '/static'
