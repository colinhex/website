import flask
from flask import Blueprint, render_template, request
from .utils.forms import RegisterForm, LoginForm
from .utils.security import is_safe_redirect
import logging
import sys

app = None
hub = Blueprint('hub', __name__, static_folder='static')

Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(
    stream=sys.stdout,
    filemode="w",
    format=Log_Format,
    level=logging.DEBUG
)

logger = logging.getLogger()


@hub.route("/")
def index():
    return render_template('index.html')


@hub.route("/signin", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        next_site = None
        if request.form['submit'] == 'register':
            if RegisterForm(request.form).validate():
                flask.flash('You are registered!')
                next_site = flask.request.args.get('next')
        elif request.form['submit'] == 'login':
            if LoginForm(request.form).validate():
                flask.flash('You are logged in!')
                next_site = flask.request.args.get('next')
        else:
            return flask.abort(400)
        if not is_safe_redirect(next_site, app):
            return flask.abort(400)
        return flask.abort(200)
    elif request.method == 'GET':
        return render_template('signin.html')
    else:
        return flask.abort(400)


@hub.route("/updates")
def blog():
    blog_post = {
        'bpid': 'bp_0',
        'title': 'What a day!',
        'date': '1.1.2022',
        'author': 'hypenguin',
        'txt': 'test blogpost from meeee',
        'href': '/static/img/email.jpg',
        'commentable': 'true'
    }
    blog_comment = {
        'cid': 'c_0',
        'predecessor': 'bp_0',
        'date': '12.01.2022',
        'author': 'Marcel Lüthi',
        'txt': 'And you can comment',
        'commentable': 'true'
    }
    blog_comment_successor = {
        'cid': 'c_1',
        'predecessor': 'c_0',
        'date': '12.01.2022',
        'author': 'Marcel Lüthi',
        'txt': 'And comment on comments!',
        'commentable': 'true'
    }
    return render_template('blog.html', blog_posts=[blog_post], blog_comments=[blog_comment, blog_comment_successor])

