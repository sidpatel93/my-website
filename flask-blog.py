from flask import Flask, render_template

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)