import base64
from datetime import datetime, timedelta
from hashlib import md5
# i'm using the md5 for generating a unique identity for the avatars
import os, json, jwt
from time import time
from flask import current_app, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login, search

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
    def checkToken(token):
        user = User.query.filter_by(token=token).first() 
        if user is None or user.token_expiration_date < datetime.utcnow():
            return None
        return user

class User(UserMixin, TokenMixin, db.Model):
    __searchable__ = ['institution', 'department']
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(32))
    lastname = db.Column(db.String(32))
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    institution = db.Column(db.String(64))
    department = db.Column(db.String(64))
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    pwhash = db.Column(db.String(128))
    projects = db.relationship('Project', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<user:{} name:{} {}>'.format(self.username, self.firstname, self.lastname)

    def setPassword(self, password):
        self.pwhash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.pwhash, password)

    # This function retrieves an avatar for users using their emails. These 
    # avatars will be used as user profile pictures. It has been redacted for now,
    # pending approval from group members.
    #
    # def avatar(self, size):
    #     digest = md5(self.email.lower().encode('utf-8')).hexdigest()
    #     return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
    #         digest, size)    
    

    def toDict(self, inc_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'institution': self.institution,
            'department': self.department,
            #'avatar': self.avatar(128)
            'project_count': self.projects.count()
        }
        if inc_email:
            data['email'] = self.email
        return data

    def fromDict(self, data, new_user=False):
        for field in ['username', 'email', 'firstname', 'lastname', 'school',
                'department']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.setPassword(data['password'])

# class Lecturer(User, UserMixin, TokenMixin, db.Model):
#     projects = db.relationship('Project', backref='inspector', lazy='dynamic')
#     #include columns for lecturer validation

#     def lecturerToDict(self, include_email=False):
#         data = self.toDict(include_email)
#         data['projects_count'] = self.projects.count()
#         return data

# class Student(User, UserMixin, TokenMixin, db.Model):
#     projects = db.relationship('Project', backref='author', lazy='dynamic')
#     #check with frontend guys to see if there are other info particular to students

#     def studentToDict(self, include_email=False):
#         data = self.toDict(include_email)
#         data['projects_count'] = self.projects.count()

'''Remember to include a projects_list part in the *ToDict functions after defining 
 a toDict function to handle projects. The list should be a dict of all projects submitted or supervised by a user.
'''

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    #return Lecturer.query.get(int(id)) or Student.query.get(int(id))

class Project(db.Model):
    __searchable__ = ['title', 'authors', 'publish_date']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    authors = db.Column(db.String(250))
    #approved = db.Column(db.Boolean, default=False)
    submit_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    publish_date= db.Column(db.DateTime, index=True)
    file_data= db.Column(db.LargeBinary)
    filename = db.Column(db.String(120), unique=True)
    owner = db.Column(db.Integer, db.ForeignKey('student.id'))
    supervisor = db.Column(db.Integer, db.ForeignKey('lecturer.id'))
    #requested_approval = db.Column(db.Boolean, default=False)
    #approval_req_accepted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<{}>'.format(self.title)
    

    # Remove these methods from here and implement them appropriately in their respective view modules.
    #
    # def approve(self):
    #     self.approved = True
    #     self.publish_date = datetime.utcnow
    #
    # def requestApproval(self):
    #     self.requested_approval = True
    #     '''return true
    #     remember to uncomment this return statement when implementing logic to
    #     ensure an approval request is submitted once'''
    #
    # def acceptApprovalRequest(self):
    #     self.approval_req_accepted = True
    #
    # def isPendingApproval(self):
    #     if self.requested_approval and not self.approval_req_accepted:
    #         return True
    #     return False

    def hashFilename(self, filename):
        digest = md5(filename.lower().encode('utf-8')).hexdigest()
        self.filename = digest

    def toDict(self, public=True):
        data = {
            'id': self.id,
            'title': self.title,
            'date_published': self.publish_date, 
            'author_id': self.owner,
            'author': self.author
        }
        if not public:
            data['date_submitted'] = self.submit_date
            data['supervisor_id'] = self.supervisor
            data['supervisor'] = self.inspector
        return data

    # The static method below will pass a specified no. of projects per page into a 
    # dictionary that will be passed into a json response object for the allowed 
    # routes. Resturcture the '_links' property to suite the requirements from the 
    # frontenders.
    # Nonetheless, I have commented the block out since I was looking at another 
    # implementation where we leave the pagination to the client-side, thus 
    # returning anything from the database that matches the query in the response 
    # object on the very first request
    #
    # @staticmethod
    # def to_collection_dict(query, page, per_page, endpoint, **kwargs):
    #     resources = query.paginate(page, per_page, False)
    #     data = {
    #         'projects': [project.to_dict() for project in resources.projects],
    #         '_meta': {
    #             'page': page,
    #             'per_page': per_page,
    #             'total_pages': resources.pages,
    #             'total_items': resources.total
    #         },
    #         '_links': {
    #             'self': url_for(endpoint, page=page, per_page=per_page,
    #                             **kwargs),
    #             'next': url_for(endpoint, page=page + 1, per_page=per_page,
    #                             **kwargs) if resources.has_next else None,
    #             'prev': url_for(endpoint, page=page - 1, per_page=per_page,
    #                             **kwargs) if resources.has_prev else None
    #         }
    #     }
    #     return data
            
    