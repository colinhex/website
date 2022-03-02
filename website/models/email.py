from flask_mail import Mail, Message
from flask import url_for, render_template
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
        'Hello! Verify your email address on {}...'.format(preferences['WEBSITE_NAME']),
        sender=preferences['MAIL_USERNAME'],
        recipients=[address]
    )
    logger.debug(preferences)
    logger.debug(user_data)
    msg.html = render_template(
        'verification_email.html',
        domain=preferences['DOMAIN'],
        website_name=preferences['WEBSITE_NAME'],
        user_id=user_data['user_id'],
        token=preferences['DOMAIN'] + '/confirm/' + generate_token(address) + '/' + user_data['user_id']
    )
    email_manager.send(msg)

