#all app configurations will be put in this module

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '$change-me$'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PROJECTS_PER_PAGE = 10
    WHOOSH_BASE = os.path.join(basedir, 'whoosh_base')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'knights.of.coe3@gmail.com'
    MAIL_PASSWORD = 'coe3solutionarchitects'
    ADMINS = ['knights.of.coe3@gmail.com']
