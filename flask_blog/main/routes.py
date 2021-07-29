from flask import Blueprint, render_template, request
from flask_blog.models import Post
main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home_page():
    # Implement the pagination to show 5 pages at a time.
    # default page will be page 1

    page = request.args.get('page', 1, type=int)
    # paginate the pages by order the post are created.
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page=5)
    return render_template('home.html', posts = posts)

@main.route('/about')
def about_page():
    return render_template('about.html', title='About')