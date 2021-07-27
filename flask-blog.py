from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config["SECRET_KEY"] = 'a66091b86cdc29fe0c984b07dd582274'

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
def registration_page():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form = form)

@app.route('/login')
def login_page():
    form = LoginForm()
    return render_template('login.html', title='Login Page', form = form)

if __name__ == '__main__':
    app.run(debug=True)