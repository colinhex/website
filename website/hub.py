import flask_login
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from flask_login import LoginManager, login_user, logout_user, current_user

import logging
import sys
import json

from .utils.forms import RegisterForm, LoginForm, PostForm, CommentForm, ContactForm
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


# --------- Request Tracking -----------

def track_request(_request):
    data = {
        'user_id': current_user.get_id(),
        'ip': _request.remote_addr,
        'ua': _request.user_agent,
        'url-root': _request.url_root,
    }

    # Todo to database


def log_request_details(_request):
    logger.debug('{}: \n {}'.format(_request.url_root, json.dumps(request.form, indent=4)))


# ---------- Routes ----------

@hub.route("/")
def index():
    track_request(request)
    log_request_details(request)
    if 'logged_in' not in session:
        session['logged_in'] = False
    return render_template('index.html')


@hub.route("/register", methods=['GET', 'POST'])
def register():
    track_request(request)
    log_request_details(request)

    if request.method == 'POST':
        if session['logged_in']:
            logger.debug('Already logged in...')
            return redirect(url_for('hub.login'), code=303)

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

            logger.debug('Successfully registered new user...')
            flash('You are registered! Verify your email to login...')
            next_site = url_for('hub.index')
        else:
            logger.debug('Form Errors: ' + str(form.errors))
            flash('Form not validated...')
            return render_template('register.html')  # Todo Show why not validated

        logger.debug(next_site)
        # Check Redirect
        if not security.is_safe_redirect(next_site, app):
            return abort(400)

        return redirect(next_site)

    elif request.method == 'GET':
        if 'logged_in' in session and session['logged_in']:
            flash('You are already logged in...')
            return redirect(url_for('hub.index'))
        return render_template('register.html')

    else:
        return abort(400)


@hub.route("/confirm/<token>/<user_id>")
def confirm_email(token, user_id):
    track_request(request)
    log_request_details(request)
    try:
        address = security.confirm_verification_token(token)
    except ValueError:
        logger.debug('Token expired...')
        flash('token has expired', 'danger')
        return abort(400)
    user = User.get_user(user_id)
    if not user.is_anonymous() and user.activate(address):
        flash('Success!')
        logger.debug('Successfully confirmed email address...')
        session['logged_in'] = False
        return redirect(url_for('hub.login'))
    else:
        flash('Could not verify...')
        logger.debug('No verification was possible...')
        return abort(400)


@hub.route('/login', methods=['GET', 'POST'])
def login():
    track_request(request)
    log_request_details(request)
    if request.method == 'GET':
        if 'logged_in' in session and session['logged_in']:
            flash('You are already logged in...')
            return redirect(url_for('hub.index'))
        return render_template('login.html')

    elif request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
            logger.debug('Login Form Validated...')

            user = User.get_user(request.form['username'])
            user.authenticate(request.form['password'])

            if login_user(user):
                flash('You are logged in!')
                logger.debug('Logged in user...')
                session['logged_in'] = True
                next_site = url_for('hub.index')
            else:
                flash('Could not log you in...')
                return render_template('login.html')  # Todo Show why not validated
        else:
            logger.debug('Form Errors: ' + str(form.errors))
            flash('Form not validated...')
            return render_template('login.html')  # Todo Show why not validated

        logger.debug(next_site)

        # Check Redirect
        if not security.is_safe_redirect(next_site, app):
            return abort(400)

        return redirect(next_site)
    else:
        return abort(400)


@hub.route("/logout")
def logout():
    track_request(request)
    log_request_details(request)
    logout_user()
    session['logged_in'] = False
    logger.debug('Logged out user...')
    return redirect(url_for('hub.index'))


@hub.route("/updates", methods=['GET', 'POST'])
def updates():
    track_request(request)
    log_request_details(request)
    if request.method == 'POST':
        if not session['logged_in']:
            logger.debug('Not logged in...')
            return redirect(url_for('hub.login'), code=303)
        post_form = PostForm(request.form)
        comment_form = CommentForm(request.form)
        if post_form.validate():
            logger.debug('Update Post Form Validated')
            queries.create_post(
                current_user.get_id(), request.form['title'], request.form['text'], request.form['link']
            )
            return redirect(url_for('hub.updates'), code=303)
        elif comment_form.validate():
            logger.debug('Update Comment Form Validated')
            queries.create_comment(
                current_user.get_id(), request.form['text'], request.form['parent']
            )
            return redirect(url_for('hub.updates'), code=303)
        else:
            logger.debug('PostForm E: {}, CommentForm E: {}'.format(post_form.errors, comment_form.errors))
            abort(400)

    elif request.method == 'GET':

        posts = queries.get_posts('blog_loader')
        comments = queries.get_comments('blog_loader')

        return render_template('updates.html', blog_posts=posts, blog_comments=comments)
    else:
        return abort(400)


@hub.route("/settings")
@flask_login.login_required
def settings():
    track_request(request)
    log_request_details(request)
    return render_template('settings.html')


@hub.route("/share/<url>")
def share():
    track_request(request)
    log_request_details(request)
    pass


@hub.route("/reddit-comments")
def reddit_comments_embedded():
    return render_template('rcomments.html')
