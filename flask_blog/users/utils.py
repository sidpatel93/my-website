import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from flask_blog import app, mail

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

def send_reset_email(user):
    '''This function will send the email to user'''
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link: {url_for('users.reset_token', token = token, _external = True)}
    If you did not make this request, please ignore this request and no changes will be made.
    '''
    mail.send(msg)