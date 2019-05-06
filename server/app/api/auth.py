from flask import g
from flask_login import current_user
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import Lecturer, Student
from app.api.errors import errorResponse

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(username, password):
    user = Lecturer.query.filter_by(username=username).first() or Student.query.filter_by(username=username).first()
    if user is None:
        return False
    g.current_user = user
    return user.checkPassword(password)

@basic_auth.error_handler
def basicAuthError():
    return errorResponse(401)


@token_auth.verify_token
def verify_token(token):
    g.current_user = Lecturer.checkToken(token) or Student.checkToken(token) if token else None
    return g.current_user is not None

@token_auth.error_handler
def tokenAuthError():
    return errorResponse(401)