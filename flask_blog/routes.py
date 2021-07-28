from flask import render_template, url_for, flash, redirect
from flask_blog import app
from flask_blog.forms import RegistrationForm, LoginForm
from flask_blog.models import User, Post

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
    form = RegistrationForm()

    if form.validate_on_submit():
        flash(f'Accounted created for {form.username.data} !', category='success')
        return redirect(url_for('home_page'))
    return render_template('register.html', title='Register', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'sid@gmail.com' and form.password.data == '123':
            flash('You have been logged in!', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Login unsuccessful, Please check username and password', category='danger')
    return render_template('login.html', title='Login Page', form = form)