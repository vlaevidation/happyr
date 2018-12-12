from flask import Flask
from app.db import DB

def create_app():
    app = Flask(__name__, static_url_path="/static")

    @app.route("/users", methods=["POST"])
    def signup():
        pass

    @app.route("/message", methods=["POST"])
    def message_users():
        # Send a message to all users
        pass

    @app.route("/response", methods=["POST"])
    def handle_response():
        # Webhook for the user texting us / twilio hits this
        pass

    DB.init_app(app)

    return app

if __name__ == "__main__":
    create_app()
