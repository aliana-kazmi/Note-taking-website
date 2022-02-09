from flask import Blueprint, redirect, render_template, request, flash, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_url, login_required, login_user, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    #data_req = request.form.get('___') #data that was sent as part of form will be kept in data
    if request.method == 'POST':
        user_name = request.form.get('userName')
        password = request.form.get('password')
        #checking if the user exists

        user = User.query.filter_by(user_id=user_name).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('Logged in successfully!', category='success')
                
                return redirect(url_for('views.home'))
            else:
                flash('Log-in failed. Check your password', category='error')
        else:
            flash('User name does not exist. Check your username', category='error')
    
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required    
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        user_name = request.form.get('userName')
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        pass_confirm = request.form.get('password2')
        user_name_check = User.query.filter_by(user_id=user_name).first()
        email_check = User.query.filter_by(email = email).first()
        if user_name_check:
            flash('User name already exists. Try another user name', category='error')
        elif email_check:
            flash('Email already in use. Enter another email.', category='error')
        elif len(email) < 4:
            flash('Invalid email. Length is smaller than expected length', category = 'error')
        elif len(first_name) < 2:
            flash('Error. First name should be longer than 1 characters', category = 'error')
        elif len(password1) < 7:
            flash('Password length short!!! 7 charactersrequired for password', category = 'error')
        elif password1 != password2:
            flash('Password do not match!!!', category = 'error')
        else:
            #add user yo database
            new_user = User(user_id=user_name, email=email, firstName = first_name, password = generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', category = 'success')
            login_user(new_user, remember=True)
            #calls the home() function of views.py
            return redirect(url_for('views.home'))


    return render_template("sign_up.html", user=current_user)