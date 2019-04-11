from flask import jsonify, request, url_for
from app import db
from app.models import Lecturer
from app.api import bp

'''Refactor the routes in the various view functions to match the pages and links
provided in the frontend. The routes used here are strictly for development and 
testing purposes, though some might stay the same should the suite a link/page in
the frontend.
'''

@bp.route('/lecturer/<int:id>', methods=['GET'])
def getUser(id):
    return jsonify(Lecturer.query.get_or_404(id).lecturerToDict(True))
    #True is passed to include email in response

@bp.route('/lecturer', methods=['POST'])
def createUser():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return 'provide a username, password and email'
    if Lecturer.query.filter_by(username=data['username']).first():
        return 'use a different username'
    if Lecturer.query.filter_by(email=data['email']).first():
        return 'use a different email'
    lecturer = Lecturer()
    lecturer.fromDict(data, new_user=True)
    db.session.add(lecturer)
    db.session.commit()
    response = jsonify(lecturer.lecturerToDict(True))
    #True is passed to include email in response; leave blank for default[false] 
    response.status_code = 201
    response.headers['Location'] = url_for('api.getUser', id=lecturer.id)
    return response