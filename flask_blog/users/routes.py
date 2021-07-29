from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_blog import db, bcrypt
from flask_blog.models import User, Post
from flask_blog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flask_blog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
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
        return redirect(url_for('users.login_page'))
    return render_template('register.html', title='Register', form = form)

@users.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home_page')) # return to next_page if it exist or return to home page if it does not.
        else:
            flash('Login unsuccessful, Please check email and password', category='danger')
    return render_template('login.html', title='Login Page', form = form)

@users.route('/logout')
def logout_page():
    logout_user()
    return redirect(url_for('main.home_page'))

@users.route('/account', methods=['GET', 'POST'])
@login_required                 # login is required to access this route. we defined the path for the login page in the __init__ file.
def account_page():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', category='success')
        return redirect(url_for('users.account_page'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/'+current_user.image_file)
    return render_template('account.html', title='Account', image_file = image_file, form = form)

@users.route('/user/<string:username>')
def user_posts(username):
    # Implement the pagination to show 5 pages at a time.
    # default page will be page 1
    page = request.args.get('page', 1, type=int)
    #
    user = User.query.filter_by(username = username).first_or_404()
    # paginate the pages by order the post are created. Line is break in to multiple lines  for ease of interpretation.
    posts = Post.query.filter_by(author = user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page = page, per_page=5)
    return render_template('user_posts.html', posts = posts, user= user)

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been send with instruction to rest the password', category='info')
        return redirect(url_for('users.login_page'))
    return render_template('reset_request.html', title = 'Reset password', form = form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'), token)
    user = User.verify_reset_token(token)
    if user is None:
        flash('This is an invalid or expired token', category='warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # Created a hashed password to from the password the user entered in the form.
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # update the password with hashed password
        user.password = hashed_password
        # Commit the password changes to the DB.
        db.session.commit()

        flash(f'Your password has been updated Successfully!', category='success')
        return redirect(url_for('users.login_page'))

    return render_template('reset_token.html', title = 'Reset password', form = form)