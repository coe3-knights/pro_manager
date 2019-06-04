from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from config import Config
import flask_whooshalchemy as w

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    #import and register blueprints here
    from app.api import bp as api
    app.register_blueprint(api)

    from app.email import bp as email
    app.register_blueprint(email)

    #import models here for whoosh indexing
    from app.models import User
    w.whoosh_index(app, User)

    from app.models import Project
    w.whoosh_index(app, Project)

    return app

from app import models
