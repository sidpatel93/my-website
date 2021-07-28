from flask import render_template, url_for, flash, redirect, request
from flask_blog import app, db, bcrypt
from flask_blog.forms import RegistrationForm, LoginForm
from flask_blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [{
    'author': 'Siddharth Patel',
    'title': 'Blog1',
    'content': 'Content for blog1',
    'date_posted': 'July 27th 2021'
},
    {
    'author': 'Vishva Patel',
    'title': 'Blog2',
    'content': 'Content for blog2',
    'date_posted': 'July 26th 2021'
    }
]


@app.route('/')
def home_page():
    return render_template('home.html', posts = posts)

@app.route('/about')
def about_page():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = RegistrationForm()

    if form.validate_on_submit():
        # Created a hashed password to store in DB.
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Created User instance to be stored in the DB.
        user = User(username=form.username.data, email=form.email.data, password = hashed_password)
        # Store the User instance in the DB.
        db.session.add(user)
        db.session.commit()

        flash(f'Your Account has been created Successfully!', category='success')
        return redirect(url_for('login_page'))
    return render_template('register.html', title='Register', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home_page')) # return to next_page if it exist or return to home page if it does not.
        else:
            flash('Login unsuccessful, Please check email and password', category='danger')
    return render_template('login.html', title='Login Page', form = form)

@app.route('/logout')
def logout_page():
    logout_user()
    return redirect(url_for('home_page'))

@app.route('/account')
@login_required                 # login is required to access this route. we defined the path for the login page in the __init__ file.
def account_page():
    return render_template('account.html', title='Account')