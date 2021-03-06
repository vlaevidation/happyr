from flask import Flask, redirect, request, \
    Response, render_template
from twilio.twiml.messaging_response import MessagingResponse
from flask.ext.heroku import Heroku
from app.db import DB
from app.models import User
from app.models import Response as UserResponse
from app.models import seed_test_data
from app.sms import send_message
import os

from app.utils import normalize_number
from app.parser import parse, respond_to

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
        send_message(body='Hello from happyr! Please respond with CONFIRM to finish your registration.', to=phone_number)

        user = User(phone_number=phone_number)
        DB.session.add(user)
        DB.session.commit()

        return render_template('signed_up.html')

    @app.route("/message", methods=["GET"])
    def message_users():
        # Note:  the .all() at the end is completely unscalable.  viva la hack day
        users = DB.session.query(User).filter(
                User.confirmed == True
                ).all()
        message = 'Hello from happyr!\nHow are you doing lately?'
        for user in users:
            try:
                send_message(body=message, to=user.phone_number)
            except Exception as e:
                print("we can't send to {}: {}".format(user.phone_number, e))
                pass

        return "Messages (presumably) sent."    # this is intended to be called from curl or similar not twilio or browser so we don't need tags

    @app.route("/happy", methods=["GET"])
    def happy():
        # List all users
        return render_template('list.html', users=User.query.all())

    @app.route("/happy/<int:id>", methods=["GET"])
    def profile(id):
        return render_template('profile.html',
            user=User.query.get(id),
            responses=UserResponse.query.filter(UserResponse.user_id == id)
        )

    @app.route("/test", methods=["GET"])
    def seed():
        seed_test_data()
        return redirect("/happy")

    @app.route("/response", methods=["GET", "POST"])
    def handle_response():
        # See: https://www.twilio.com/docs/sms/tutorials/how-to-receive-and-reply-python
        # Webhook for the user texting us / twilio hits this
        print("Request values", request.values)
        body = request.values.get('Body', None)
        phone_number = request.values.get('From')
        phone_number = normalize_number(phone_number)

        resp = MessagingResponse()

        if body.lower() == 'confirm':
            print("Looking for user with phone number {}".format(phone_number))
            user = DB.session.query(User).filter(
                User.phone_number == phone_number,
                User.confirmed == False
            ).one_or_none()
            print("query result: {}".format(user))

            if user:
                user.confirmed = True
                DB.session.add(user)
                DB.session.commit()
                resp.message("Thank you! Your path to happiness begins NOW!")
                return str(resp)
            else:
                return ''

        else:
            # check if user confirmed
            # if so do the regular response flow: store in db, thank the user
            user = DB.session.query(User).filter(
                User.phone_number == phone_number,
                User.confirmed == True
            ).one_or_none()
            print("found user: {}".format(user))
            if user:
                message = body.lower()
                try:
                    score = parse(message)
                    print("Scoring message {} as happiness level {}".format(message, score))
                except Exception as e:
                    print("Error in parsing message: {}".format(e))
                    score = None

                response = UserResponse(
                    user_id=user.id,
                    raw=body.lower(),
                    happiness=score
                )
                DB.session.add(response)
                DB.session.commit()

                response_text = respond_to(int(score))
                resp.message("{}\nThanks for sharing. Your response has been recorded.".format(response_text))
            else:
                resp.message("Please sign up and confirm first.")
            return str(resp)

    DB.init_app(app)

    return app

if __name__ == "__main__":
    create_app()
