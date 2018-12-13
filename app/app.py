from flask import Flask, request, Response, render_template
from app.db import DB
from app.models import User

def create_app(env="Development"):
    app = Flask(__name__, static_url_path="/static")
    if env == "Development":
        app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///hack18"

    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/signup", methods=["POST"])
    def signup():
        phone_number = request.form['phone_number']
        print("Received signup for phone numer {}".format(phone_number))

        # todo - persist signup to db - will require postgres up
        user = User(phone_number = phone_number)
        DB.session.add(user)
        DB.session.commit()

        return render_template('signed_up.html')

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
