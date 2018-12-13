from flask import Flask, request, Response, render_template
from app.db import DB
from app.sms import confirm_user

def create_app():
    app = Flask(__name__, static_url_path="/static")

    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/signup", methods=["POST"])
    def signup():
        phone_number = request.form['phone_number']
        print("Received signup for phone number {}".format(phone_number))
        confirm_user(body='Hello from happyr!', to=phone_number)
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
