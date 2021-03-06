from flask import render_template, flash, redirect, url_for, session, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from blogapp import app, db
from blogapp.forms import LoginForm, SignupForm, ProfileForm, PostForm
from blogapp.models import User,Post, Profile
from blogapp.config import Config
import os, time

@app.route('/')
@app.route('/index')
def index():
	user = {'username': 'Vivek'}
	return render_template('index.html', title='Home', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user_in_db = User.query.filter(User.username == form.username.data).first()
		if not user_in_db:
			flash('No user found with username: {}'.format(form.username.data))
			return redirect(url_for('login'))
		if (check_password_hash(user_in_db.password_hash, form.password.data)):
			flash('Login success!')
			session["USERNAME"] = user_in_db.username
			return render_template('choice.html', user=user_in_db)
		flash('Incorrect Password')
		return redirect(url_for('login'))
	return render_template('login.html', title='Sign In', form=form)
	
@app.route('/checkuser', methods=['POST'])
def check_username():
	chosen_name = request.form['username']
	user_in_db = User.query.filter(User.username == chosen_name).first()
	if not user_in_db:
		return jsonify({'text': 'Username is available',
						'returnvalue': 0})
	else:
		return jsonify({'text': 'Sorry! Username is already taken',
						'returvalue': 1})
	
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()
	if form.validate_on_submit():
		if form.password.data != form.password2.data:
			flash('Passwords do not match!')
			return redirect(url_for('signup'))
		passw_hash = generate_password_hash(form.password.data)
		user = User(username=form.username.data, email=form.email.data, password_hash=passw_hash)
		db.session.add(user)
		db.session.commit()
		flash('User registered with username:{}'.format(form.username.data))
		session["USERNAME"] = user.username
		return render_template('choice.html', user=user)
	return render_template('signup.html', title='Register a new user', form=form)
	
@app.route('/profile', methods=['GET', 'POST'])
def profile():
	form = ProfileForm()
	if not session.get("USERNAME") is None:
		if form.validate_on_submit():
			cv_dir = Config.CV_UPLOAD_DIR
			file_obj = form.cv.data
			cv_filename = session.get("USERNAME") + '_CV.pdf'
			file_obj.save(os.path.join(cv_dir, cv_filename))
			flash('CV uploaded and saved')
			# now we add the object to the database
			user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
			#check if user already has a profile
			stored_profile = Profile.query.filter(Profile.user == user_in_db).first()
			if not stored_profile:
				# if no profile exists, add a new object
				profile = Profile(dob=form.dob.data, gender=form.gender.data, cv=cv_filename,user=user_in_db)
				db.session.add(profile)
			else:
				# else, modify the existing object with form data
				stored_profile.dob = form.dob.data
				stored_profile.gender = form.gender.data
			# remember to commit	
			db.session.commit()
			return redirect(url_for('choice'))
		else:
			user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
			stored_profile = Profile.query.filter(Profile.user == user_in_db).first()
			if not stored_profile:
				return render_template('profile.html', title='Add your profile', form=form)
			else:
				form.dob.data = stored_profile.dob
				form.gender.data = stored_profile.gender
				return render_template('profile.html', title='Modify your profile', form=form)
				
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))
		
@app.route('/choice')
def choice():
	if not session.get("USERNAME") is None:
		user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
		return render_template('choice.html', user=user_in_db)
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))
	
		
@app.route('/post', methods=['GET', 'POST'])
def post():
	form = PostForm()
	if not session.get("USERNAME") is None:
		if form.validate_on_submit():
			body = form.postbody.data
			user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
			post = Post(body=body, author = user_in_db)
			db.session.add(post)
			db.session.commit()
			return redirect(url_for('post'))
		else:
			user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
			prev_posts = Post.query.filter(Post.user_id == user_in_db.id).all()
			print("Checking for user: {} with id: {}".format(user_in_db.username, user_in_db.id))
			return render_template('post.html', title='User Posts', prev_posts=prev_posts, form=form)
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))
		
@app.route('/logout')
def logout():
	session.pop("USERNAME", None)
	return redirect(url_for('login'))