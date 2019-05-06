from flask import jsonify, request, url_for
from app import db
from app.models import Lecturer
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import badRequest

'''Refactor the routes in the various view functions to match the pages and links 
 provided in the frontend. The routes used here are strictly for development and 
 testing purposes, though some might stay the same should the suite a link/page in 
 the frontend.
'''


'''The view function below returns lecturer information on the current user(that is 
 why True is passed to the lectToDict method). Though they have similar technicalities, I have not explicitly handled the data that will be sent when a client request information on a different user. This is because, that functionality has not been set to be included in our product.
'''
@bp.route('/lecturer/<string:username>', methods=['GET'])
@token_auth.login_required
def getUser(username):
    return jsonify(Lecturer.query.get_or_404(username).lecturerToDict(True))
    #True is passed to include email in response


''' This createUser view function handles user sign-ups. I have left out rejecting 
 null values for fields other than the ones implemented here, to be done in the frontend design.
'''
@bp.route('/lecturer', methods=['POST'])
def createUser():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return badRequest('provide a username, password and email')
    if Lecturer.query.filter_by(username=data['username']).first():
        return badRequest('username is already taken')
    if Lecturer.query.filter_by(email=data['email']).first():
        return badRequest('email address already used!')
    lecturer = Lecturer()
    lecturer.fromDict(data, new_user=True)
    db.session.add(lecturer)
    db.session.commit()
    response = jsonify(lecturer.lecturerToDict(True))
    #True is passed to include email in response; leave blank for default[false] 
    response.status_code = 201
    response.headers['Location'] = url_for('api.getUser', id=lecturer.id)
    return response

#This view function is self explanatory right? ;)
@bp.route('/lecturer/<string:username>', methods=['PUT'])
@token_auth.login_required
def updateUser(username):
    lecturer = Lecturer.query.get_or_404(username)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != lecturer.username and Lecturer.query.filter_by(username=data['username']).first():
        return badRequest('please use a different username')
    if 'email' in data and data['email'] != lecturer.email and Lecturer.query.filter_by(email=data['email']).first():
        return badRequest('please use a different email address')
    lecturer.fromDict(data)
    db.session.commit()
    return jsonify(lecturer.lecturerToDict())
