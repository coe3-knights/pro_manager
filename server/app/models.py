import base64
from datetime import datetime, timedelta
from hashlib import md5
import os, json, jwt
from time import time
from flask import current_app, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login

'''Recheck the implementation of the database schema: all relationships in here now are one to one.
Association table for the relationship between either three models have not been created yet. This is 
because I have not received any of your schemas yet and I do not want to veto on which one we should
use. Feel free to edit this current model and push to the branch I have created for this situation's 
pull request. Please, ensure that you do not push to the main branch as this might cause inconsistency
on our various machines. Read the Flask_sqlalchemy documentation(version 2.3) if you do not understand 
anything in this code.  '''
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

    def set_password(self, password):
        self.pwhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwhash, password)

    ''' This function retrieves an avatar for users using their emails. These avatars will be used as 
    user profile pictures. It has been redacted for now, pending approval from group members.

            def avatar(self, size):
                digest = md5(self.email.lower().encode('utf-8')).hexdigest()
                return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)    
    '''

class Lecturer(User, UserMixin, db.Model):
    projects = db.relationship('Project', backref='inspector', lazy='dynamic')
    #include columns for lecture validation

class Student(User, UserMixin, db.Model):
    projects = db.relationship('Project', backref='author', lazy='dynamic')
    #check with frontend guys to see if there are other info particular to students

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

    def request_approval(self):
        self.requested_approval = True
        '''return true
        remember to uncomment this return statement when implementing logic to ensure an 
        approval request is submitted once'''
    
    def accept_approval_req(self):
        self.approval_req_accepted = True

    def is_pending_approval(self):
        if self.requested_approval and not self.approval_req_accepted:
            return True
        return False