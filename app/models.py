from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    books = db.relationship('Books', backref='issued_by', lazy='dynamic')
    occupation = db.Column(db.String(64),default="student")
    subject=db.Column(db.String(64))
    random=db.Column(db.String(120),index=True,unique=True,default=None)
    #due_of = db.relationship('Due', backref='issuer', lazy='dynamic')

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
	    if check_password_hash(self.password_hash, password):
		    session['username']=self.username
	    return check_password_hash(self.password_hash, password)

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(400), index=True, unique=True)
    author = db.Column(db.String(140), index=True, unique=True)
    #no_copies = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #book_due = db.relationship('Due', backref='book_due', lazy='dynamic')
    due=db.Column(db.Date)
    btype=db.Column(db.String(140),index=True)
    img = db.Column(db.String(2000))

    def __repr__(self):
        return '<Book: {},{}>'.format(self.book_name,self.author)
