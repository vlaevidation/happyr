from flask import Flask, request, Response, render_template
from twilio.twiml.messaging_response import MessagingResponse
from flask.ext.heroku import Heroku
from app.db import DB
from app.models import User
from app.sms import confirm_user
import os


def create_app(env="Development"):
    app = Flask(__name__, static_url_path="/static")

    heroku = Heroku(app)

    if env == "Development":
        app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///hack18"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DATABASE_URL']

    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/signup", methods=["POST"])
    def signup():
        phone_number = request.form['phone_number']
        print("Received signup for phone number {}".format(phone_number))
        confirm_user(body='Hello from happyr! Please respond with CONFIRM to finish your registration.', to=phone_number)

        user = User(phone_number=phone_number)
        DB.session.add(user)
        DB.session.commit()

        return render_template('signed_up.html')

    @app.route("/message", methods=["POST"])
    def message_users():
        # Send a message to all users
        pass

    @app.route("/response", methods=["GET", "POST"])
    def handle_response():
        # See: https://www.twilio.com/docs/sms/tutorials/how-to-receive-and-reply-python
        # Webhook for the user texting us / twilio hits this
        print("Request values", request.values)
        body = request.values.get('Body', None)
        phone_number = request.values.get('From')

        resp = MessagingResponse()

        if body.lower() == 'confirm':
            # TODO: we will need some normalization of phone numbers
            user = DB.session.query(User).filter(
                User.phone_number == phone_number,
                User.confirmed == False
            ).one_or_none()
            print("query result: {}".format(user))

            if user:
                user.confirmed = True
                DB.session.add(user)
                DB.session.commit()
                resp.message("Thank you!w Your path to happiness begins NOW!")
                return str(resp)
            else:
                return ''

        else:
            # check if user confirmed
            # if so do the regular response flow: store in db, thank the user
            pass

    DB.init_app(app)

    return app

if __name__ == "__main__":
    create_app()
