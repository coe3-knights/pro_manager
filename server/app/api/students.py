from flask import jsonify, request, url_for, current_app
from app import db
from app.models import User
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import badRequest
from app.email.email import sendPaswordRequest, sendEmail
from flask_login import current_user

'''Refactor the routes in the various view functions to match the pages and links 
 provided in the frontend. The routes used here are strictly for development and 
 testing purposes, though some might stay the same should the suite a link/page in 
 the frontend.
'''


# The view function below returns student information on a user(the previous version handled that of the current user only)
@bp.route('/student/<string:username>', methods=['GET'])
@token_auth.login_required
def getUser(username):
    user = User.query.filter_by(username=username).first()
    if user == current_user:
        return jsonify(user.toDict(inc_email=True))
    return jsonify(user.toDict())


#  This createUser view function handles user sign-ups. I have left out rejecting 
#  null values for fields other than the ones implemented here, to be done in the frontend design.
@bp.route('/student/sign_up', methods=['POST'])
def createUser():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return badRequest('no username, password or email')
    if User.query.filter_by(username=data['username']).first():
        return badRequest('username is already taken')
    if User.query.filter_by(email=data['email']).first():
        return badRequest('email address already used!')
    student = User()
    student.fromDict(data, new_user=True)
    db.session.add(student)
    db.session.commit()
    response = jsonify(student.toDict(inc_email=True))
    #True is passed to include email in response; leave blank for default[false] 
    response.status_code = 201
    response.headers['Location'] = url_for('api.getUser', id=student.id)
    return response


@bp.route('/login', methods=['POST'])
def login():
    pass


@bp.route('/logout')
def logout():
    pass

#This view function is self explanatory right? ;)
@bp.route('/student/<string:username>/profile', methods=['PUT','GET'])
@token_auth.login_required
def updateUser(username, response):
    if request.method == 'PUT':
        student = User.query.filter_by(username=username).first()
        data = request.get_json() or {}
        if 'username' in data and data['username'] != student.username and User.query.filter_by(username=data['username']).first():
            return badRequest('please use a different username')
        if 'email' in data and data['email'] != student.email and User.query.filter_by(email=data['email']).first():
            return badRequest('please use a different email address')
        student.fromDict(data)
        db.session.commit()
        response.status_code = 201
        response.headers['Location'] = url_for('api.updateUser', username=student.username)
    response = jsonify(student.toDict())
    response.status_code = 200
    return response


@bp.route('/student/request_password_reset', methods=['POST'])
def requestPasswordReset(response):
    req_data = request.get_json()
    if 'email' not in req_data:
        return badRequest('user email required')
    user = User.query.filter_by(email=req_data['email']).first()
    if user:
        sendPaswordRequest(user)
        response.status_code = 201
        response.headers['Location'] = url_for('api.login')
        return response
    return badRequest('email not registered')


@bp.route('/student/reset_password/<token>', methods=['GET','POST'])
def resetPassword(token):
    if current_user.is_authenticated:
        return jsonify('user already logged in'), 403
    user = User.verifyPasswordResetToken(token)
    if not user:
        return jsonify('user token expired or invalid'), 403
    new_password = request.get_json['new_password']
    user.setPassword(new_password)
    db.session.commit()
    return 201


@bp.route('/student/<string:username>/search')
@token_auth.login_required
def search():
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q').paginate(page, current_app.config['POST_PER_PAGE'], False)
    payload = User.query.whoosh_search
    response = jsonify(payload)
    return response


    
# This mehthod should return all the uploads done or supervised by a user
#
# @bp.route('/<string:username>/uploads')
# @token_auth.login_required
# def userUploads():
#     pass