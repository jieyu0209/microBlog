from datetime import datetime
from blogapp import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	profile = db.relationship('Profile', backref='user', lazy='dynamic')

	def __repr__(self):
		return '<User {}>'.format(self.username)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post made on {}: {}>'.format(str(self.timestamp)[0:10],self.body)
		
class Profile(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	dob = db.Column(db.DateTime, index=True)
	gender = db.Column(db.String(10), index=True)
	cv = db.Column(db.String(256))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	
	def __repr__(self):
		return '<Profile for user: {}, gender: {}, birthday: {}>'.format(self.user_id, self.dob, self.dob)
		
	
		
