
import flask
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user

import logging
import sys
import traceback
import json

from .utils.forms import RegisterForm, LoginForm
from .utils import security
from .models.user import User
from .models import email
from website.db import queries

# ---------- Preferences ----------
__preferences = None


def set_pref(preferences):
    global __preferences
    __preferences = preferences

    security.set_pref(preferences)
    queries.set_pref(preferences)

    email.configure_app_for_email(app, preferences)


# ---------- Routing Blueprint & Application ----------

app = None
hub = Blueprint('hub', __name__, static_folder='static')

# ---------- Logging Setup ----------

Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(
    stream=sys.stdout,
    filemode="w",
    format=Log_Format,
    level=logging.DEBUG
)

logger = logging.getLogger()


# ---------- LogIn Manager ----------

login_manager = LoginManager()


def init_login_manager():
    global login_manager
    login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get_user(user_id)


# ---------- Routes ----------

@hub.route("/")
def index():
    logger.debug(request.remote_addr)
    logger.debug(request.remote_user)
    logger.debug(request.user_agent)
    logger.debug(request.url_root)
    return render_template('index.html')


@hub.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        next_site = None
        if request.form['submit'] == 'register':
            logger.debug('Register Request: \n {}'.format(json.dumps(request.form, indent=4)))
            form = RegisterForm(request.form)

            if form.validate():
                logger.debug('Register Form Validated...')

                queries.create_user(
                    request.form['username'],
                    request.form['email'],
                    request.form['password'],
                    security.hash_password,
                    security.encrypt_data
                )

                email.send_email_verification(
                    queries.get_user(request.form['username']),
                    __preferences,
                    security.generate_verification_token,
                    security.decrypt_data
                )

                for line in traceback.format_stack():
                    logger.debug(line)

                flask.flash('You are registered! Verify your email to login...')
                next_site = url_for('hub.index')
            else:
                logger.debug('Form Errors: ' + str(form.errors))

        elif request.form['submit'] == 'login':
            logger.debug('Login Request: \n {}'.format(json.dumps(request.form, indent=4)))

            form = LoginForm(request.form)
            if form.validate():
                logger.debug('Login Form Validated...')

                user = User.get_user(request.form['username'])
                user.authenticate(request.form['password'])

                if login_user(user):
                    flask.flash('You are logged in!')
                    next_site = url_for('hub.index')
                else:
                    flask.flash('Could not log you in...')
                    return render_template('register.html')
            else:
                logger.debug('Form Errors: ' + str(form.errors))
        else:
            return render_template('register.html')

        logger.debug(next_site)
        # Check Redirect
        if not security.is_safe_redirect(next_site, app):
            return flask.abort(400)

        return redirect(next_site)

    elif request.method == 'GET':
        return render_template('register.html')

    else:
        return flask.abort(400)


@hub.route("/confirm/<token>")
def confirm_email(token):
    try:
        address = security.confirm_verification_token(token)
    except ValueError:
        flask.flash('token has expired', 'danger')
        return flask.abort(400)
    user = User.from_mail(address)
    if not user.is_anonymous() and user.activate():
        flask.flash('Success!')
        return redirect('/register')
    else:
        flask.flash('Could not verify...')
        return flask.abort(400)


@hub.route("/logout")
def logout():
    logout_user()
    return render_template('index.html')


@hub.route("/updates", methods=['GET', 'POST'])
def blog():
    if request.method == 'POST':
        pass
    elif request.method == 'GET':

        posts = queries.get_posts('blog_loader')
        comments = queries.get_comments('blog_loader')

        return render_template('blog.html', blog_posts=posts, blog_comments=comments)
    else:
        return flask.abort(400)

