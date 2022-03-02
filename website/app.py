from flask import Flask
import argparse
import logging

import website.hub


logger = logging.getLogger('App')


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
parser.add_argument('--WEBSITE_NAME', type=str, default='colinhex.com', required=True)
parser.add_argument('--DOMAIN', type=str, default='http://localhost:8000', required=True)
parser.add_argument('--IP', type=str, default='localhost')
parser.add_argument('--PORT', type=int, default=8000)

args = parser.parse_args()

preferences = vars(args)

app = Flask(__name__)

app.debug = False
app.register_blueprint(website.hub.hub)
website.hub.app = app
website.hub.set_pref(preferences)
website.hub.init_login_manager()

app.config['SECRET_KEY'] = preferences['SECRET_KEY']

app.run(preferences['IP'], preferences['PORT'])
