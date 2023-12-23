#this is an authentification page! 
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db  
from flask_login import login_user, login_required, logout_user, current_user

#Blueprint - This is the instantiation of the Blueprint object.
#Used to organizing routes, templates, and static files into modular components.
auth = Blueprint('auth', __name__)

#This line decorates the login() function, defining a route /login within the auth Blueprint. 
#We used Get and Post request
@auth.route('/login', methods=['GET', 'POST'])
#This is the function that handles the logic when a user accesses the /login route.
def login():
    #simple if, else logic, with instructions
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            password = User.query.filter_by(password=password).first()
            if password:
                #flash function is used to send short-lived messages to the user interface. 
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
#return render_template() is a function used to render an HTML template. It typically generates a complete HTML page
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
#logout function:
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

#Get and POST methods to check email and passwords
@auth.route('/sign-up', methods=['GET', 'POST'])
#We created function called sign_up()
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
#users email check
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=password1)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

#this code is responsible for rendering the HTML template named "sign_up.html" and passing the current_user variable to that template.
    return render_template("sign_up.html", user=current_user)
