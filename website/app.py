from flask import Flask
import argparse


# ---------- Preferences ----------

parser = argparse.ArgumentParser()
parser.add_argument('--conn', type=str, required=True)
parser.add_argument('--SECRET_KEY', type=str, required=True)
parser.add_argument('--MAIL_SERVER', type=str, required=True)
parser.add_argument('--MAIL_PORT', type=str, required=True)
parser.add_argument('--MAIL_USERNAME', type=str, required=True)
parser.add_argument('--MAIL_PASSWORD', type=str, required=True)
parser.add_argument('--MAIL_USE_TLS', type=bool, default=False, required=False)
parser.add_argument('--MAIL_USE_SSL', type=bool, default=True, required=False)
parser.add_argument('--website_name', type=str, default='colinhex.com', required=True)

args = parser.parse_args()

preferences = vars(args)


def create_app(_preferences):
    _app = Flask(__name__)

    _app.debug = False

    import website.hub
    _app.register_blueprint(website.hub.hub)
    website.hub.app = _app
    website.hub.set_pref(_preferences)
    website.hub.init_login_manager()

    _app.config['SECRET_KEY'] = _preferences['SECRET_KEY']

    return _app


app = create_app(preferences)

app.run('localhost', 8000)
