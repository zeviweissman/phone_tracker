from flask import Flask
from app.routes import phones_blueprint


def create_flask_app():
    app = Flask(__name__)
    app.register_blueprint(phones_blueprint, url_prefix="/api/phone_tracker")
    return app

if __name__ == '__main__':
    app = create_flask_app()
    app.run()