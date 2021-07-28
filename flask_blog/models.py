from flask_blog import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique= True, nullable = False)
    email = db.Column(db.String(120), unique= True, nullable = False)
    image_file = db.Column(db.String(20), unique = False, nullable = False, default = 'default.jpeg')
    password = db.Column(db.String(60), unique = False, nullable = False)
    posts = db.relationship('Post', backref = 'author', lazy = True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    '''user.id is lower case, because if reference to 
    'user' table name that is created for User 
    class and it is default to class name lowercase.'''

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"