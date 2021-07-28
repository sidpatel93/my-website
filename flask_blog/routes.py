import secrets, os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flask_blog import app, db, bcrypt
from flask_blog.forms import RegistrationForm, LoginForm, UpdateAccountForm
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



def save_picture(form_picture):
    '''This function will resize the image and return the new image name to be store in DB '''
    # generate random name for the image.
    random_hex = secrets.token_hex(8)
    # split the file name to get the file extension of image
    f_name , f_ext = os.path.splitext(form_picture.filename)
    # create a new image name by combining new random name and file extension
    picture_fn = random_hex + f_ext
    # create the path name where the image will be stored
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    # Resize the image to 125 x 125 pixels
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    # Save the new image
    i.save(picture_path)
    # return the new image name so that we can use this to update the user profile image default name
    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('account_page'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/'+current_user.image_file)
    return render_template('account.html', title='Account', image_file = image_file, form = form)