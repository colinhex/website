from flask import Flask


glob_app = None


def create_app():
    app = Flask(__name__)

    app.debug = False

    import website.hub
    app.register_blueprint(website.hub.hub)
    website.hub.app = app

    return app
