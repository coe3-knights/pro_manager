import base64
from datetime import datetime, timedelta
from hashlib import md5
import os, json, jwt
from time import time
from flask import current_app, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login

'''Recheck the implementation of the database schema: all relationships in here
now are one to one. Association table for the relationship between either three
models have not been created yet. This is because I have not received any of your
schemas yet and I do not want to veto on which one we should use. Feel free to
edit this current model and push to the branch I have created for this situation's
pull request. Please, ensure that you do not push to the main branch as this might
cause inconsistency on our various machines. Read the Flask_sqlalchemy documentation
(version 2.3) if you do not understand anything in this code.
'''

class TokenMixin(object):
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration_date = db.Column(db.DateTime)

    def getToken(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration_date > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration_date = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revokeToken(self):
        self.token_expiration_date = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = Lecturer.query.filter_by(token=token).first() or Student.query.filter_by(
            token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

class User(UserMixin, object):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(32))
    lastname = db.Column(db.String(32))
    username = db.Column(db.String(64), index=True, unique=True)
    institution = db.Column(db.String(64))
    department = db.Column(db.String(64))
    email = db.Column(db.String(128), index=True, unique=True)
    pwhash = db.Column(db.String(128))

    def __repr__(self):
        return '<{}>'.format(self.firstname)

    def setPassword(self, password):
        self.pwhash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.pwhash, password)

    ''' This function retrieves an avatar for users using their emails. These 
    avatars will be used as user profile pictures. It has been redacted for now,
    pending approval from group members.

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)    
    '''

    def toDict(self, inc_email=False):
        data = {
            'username': self.username,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'institution': self.institution,
            'department': self.department,
        }
        if inc_email:
            data['email'] = self.email
        return data

    def fromDict(self, data, new_user=False):
        for field in ['username', 'email', 'firstname', 'lastname', 'institution',
                'department']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.setPassword(data['password'])

class Lecturer(User, UserMixin, TokenMixin, db.Model):
    projects = db.relationship('Project', backref='inspector', lazy='dynamic')
    #include columns for lecturer validation

    def lecturerToDict(self, include_email=False):
        data = self.toDict(include_email)
        data['projects'] = self.projects.count()
        return data

class Student(User, UserMixin, TokenMixin, db.Model):
    projects = db.relationship('Project', backref='author', lazy='dynamic')
    #check with frontend guys to see if there are other info particular to students

    def studentToDict(self, include_email=False):
        data = self.toDict(include_email)
        data['projects'] = self.projects.count()

@login.user_loader
def load_user(id):
    return Lecturer.query.get(int(id)) or Student.query.get(int(id))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    approved = db.Column(db.Boolean, default=False)
    submit_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    publish_date= db.Column(db.DateTime, index=True)
    file = db.Column(db.LargeBinary)
    owner = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    supervisor = db.Column(db.Integer, db.ForeignKey('lecturer.id'), nullable=False)
    requested_approval = db.Column(db.Boolean, default=False)
    approval_req_accepted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<{}>'.format(self.title)
    
    def approve(self):
        self.approved = True
        self.publish_date = datetime.utcnow

    def requestApproval(self):
        self.requested_approval = True
        '''return true
        remember to uncomment this return statement when implementing logic to
        ensure an approval request is submitted once'''
    
    def acceptApprovalRequest(self):
        self.approval_req_accepted = True

    def isPendingApproval(self):
        if self.requested_approval and not self.approval_req_accepted:
            return True
        return False