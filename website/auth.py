from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password, try again.', category='error')
        else:
            flash('Email doesn\'t exsist.', category='error')
            
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 character', category='error')
        elif len(first_name) < 2:
            flash('Email must be greater than 1 character', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Email must be atleast 7 character', category='error')
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                password=generate_password_hash(password1, method='sha256')
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
          
    return render_template("sign_up.html", user=current_user)

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            ## print(email)
            return redirect(url_for('auth.reset_password', email=email)) 
        else:
            flash('Email doesn\'t.', category='error')
    return render_template("forgot_password.html", user=current_user)

@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    email = request.args.get('email')
    ## print('email:', email) # Debug statement
    user = User.query.filter_by(email=email).first()
    ## print(type(user))
    ## print(user.password)
    if request.method == 'POST':
        # Retrieve the user's new password from the form data
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            flash('Passwords don\'t match', category='error')
        elif len(new_password) < 7:
            flash('Email must be atleast 7 character', category='error')
        else:
            # Hash the new password
            hashed_password = generate_password_hash(new_password, method='sha256')

            # Update the user's password in the database
            user.password = hashed_password
            ## print('password new:',user.password)
            try:
                db.session.commit()
            except Exception as e:
                print(e)

            flash('Your password has been updated!', category='success')
            # Redirect the user to the login page
            return redirect(url_for('auth.login')) 

    # If the request method is GET, render the reset password form
    return render_template('reset_password.html', user=current_user)

