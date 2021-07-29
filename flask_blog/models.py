from flask_blog import db, login_manager, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique= True, nullable = False)
    email = db.Column(db.String(120), unique= True, nullable = False)
    image_file = db.Column(db.String(20), unique = False, nullable = False, default = 'default.jpeg')
    password = db.Column(db.String(60), unique = False, nullable = False)
    posts = db.relationship('Post', backref = 'author', lazy = True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    def get_reset_token(self, expires_seconds = 1800):
        '''This function creates a time sensitive token using secret key
        and contains the payload(Dictionary in our case)'''

        s = Serializer(app.config['SECRET_KEY'], expires_seconds)
        return s.dumps({'user_id' : self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        '''This class method will take the token and return the User object with use_id in the token
        if the token is not expired.'''

        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


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