import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
	app = FlasK(__name__)
	app.config.from_object(config_class)

	db.init_app(app)
	mifǵrate.init_app(app, db)
	

from app import models
