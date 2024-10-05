from crypt import methods
from datetime import datetime
from flask import Flask, session, redirect
from flask import request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

import os

from werkzeug.serving import make_ssl_devcert

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = '4ikQNBb4VuJYa5kD6UFb5PoZX5LZ2Uh1gi-C1EMlg84'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(25), nullable=False)
    role = db.Column(db.Integer(), default=0, nullable=False)

    def __repr__(self):
        return f'<User: {self.username}>'


class Posts(db.Model):
    __tablename__ = 'Posts'
    id = db.Column(db.Integer, primary_key=True)
    post_name = db.Column(db.String(255), nullable=False)
    post_text = db.Column(db.Text(), nullable=False)
    post_image = db.Column(db.String(255), nullable=False)
    continent = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.Date(), default=datetime.utcnow)


# створюємо базу даних, використовуємо один раз,
# після створення закоментувати
with app.app_context():
    db.create_all()


# == ROUTES ==================================================

@app.route('/')
def index():
    x = session.get('username')
    return render_template('index.html', username=session.get('username'))


@app.route('/articles')
def articles():
    articles = Posts.query.all()

    return render_template('articles.html',
                            articles=articles)


@app.route('/add_post', methods = ['GET'])
def add_post():
    return render_template('add_post.html')

@app.route('/add_post', methods = ['POST'])
def add_post_form():
    if not session.get('username'):
        return redirect('/login')

    post_name = request.form['text']
    post_text = request.form['text']
    post_image = request.form['URL']
    continent = request.form['continent']

    row = Posts(post_name=post_name,
                post_text=post_text,
                post_image=post_image,
                continent=continent)
    db.session.add(row)
    db.session.commit()

    return render_template('add_post.html')



@app.route('/delete_post.html', methods=['GET', 'POST'])
def delete_post():
    if not session.get('username'):
        return redirect('/login')

    if request.method == 'POST':
        id_list = request.form.getlist('id')
        for id in id_list:
            row = Posts.query.filter_by(id=id).first()
            db.session.delete()

        db.session.commit()

    articles = Posts.query.all()
    render_template('delete_post.html', articles=articles)



@app.route('/details')
def details():
    return render_template('details.html')


@app.route('/login')
def login():
    message=''
    return render_template('login.html', message=message)


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    # session.pop('username')
    return redirect('/')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if not session.get('username'):
        return redirect('/login')

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return render_template('index.html')
    else:
        return render_template('add_user.html')


# Only for local server (deleted)
if __name__ == '__main__':
    app.run(debug=True)
