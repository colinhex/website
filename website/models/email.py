from flask_mail import Mail, Message
from flask import url_for
import logging

logger = logging.getLogger('Email Manager')

email_manager = None


def configure_app_for_email(app, preferences):
    # configure app for mail traffic
    app.config['MAIL_SERVER'] = preferences['MAIL_SERVER']
    app.config['MAIL_PORT'] = preferences['MAIL_PORT']
    app.config['MAIL_USERNAME'] = preferences['MAIL_USERNAME']
    app.config['MAIL_PASSWORD'] = preferences['MAIL_PASSWORD']
    app.config['MAIL_USE_TLS'] = preferences['MAIL_USE_TLS']
    app.config['MAIL_USE_SSL'] = preferences['MAIL_USE_SSL']
    logger.debug(app.config['MAIL_USE_TLS'])

    global email_manager
    email_manager = EmailManager(app)


class EmailManager:

    def __init__(self, app):
        self.mail = Mail(app)

    def send(self, message):
        self.mail.send(message)


def send_email_verification(user_data, preferences, generate_token, decrypt):
    address = decrypt(user_data['email'])
    msg = Message(
        'Hello! Verify your email address on {}...'.format(preferences['website_name']),
        sender=preferences['MAIL_USERNAME'],
        recipients=[address]
    )
    with open(url_for('static', filename='html/verification_mail.html')) as f:
        msg.body = f.read().format(
            preferences['DOMAIN'],
            preferences['website_name'],
            user_data['user_id'],
            preferences['DOMAIN'] + '/' + generate_token(address)
        )
    email_manager.send(msg)
