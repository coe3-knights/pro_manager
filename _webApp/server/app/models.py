#db models goes here---
from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    status = db.Column(db.Bit) #keep a bit for whehter user is a lecturer or student

class Lecturer(User):
    reference_no = db.Column(db.Integer, index=True, unique=True)
    approvals = db.relationship('Projects', backref='supervisor', lazy='dynamic')
    #add a column for lecturer verification details


class Student(User):
    index_no = db.Column(db.Integer, index=True, unique=True)
    year = db.Column(db.Integer, index=True)#year is used to store student's current year in the institution 
    projects = db.relationship('Projects', backref='author', lazy='dynamic')

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True, unique=True)
    file = db.Column(db.Binary)
    date_submitted = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    date_published = db.Column(db.DateTime, index=True)
    approved = db.Column(db.Bit, index=True)
    posted_by = db.Column(db.Integer, db.ForeignKey('index_no'))
    approved_by = db.Column(db.Integer, db.ForeignKey('reference_no'))


class Reviews(db.Model):
    pass

class Ratings(db.Model):
    pass

# The fields for the user's institution, faculty and department has been left out since 
# i am not sure whether to keep them in the 'User' model or create one for them
# I have also not defined any mehtods on the above classes given i am not done designing the 
# models and their relations. Looking forward to your contributions :)