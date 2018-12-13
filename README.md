# happyr


see:
https://dashboard.heroku.com/apps/happyr/


## Running locally

- put up a python3 venv
- `pip install -r requirements.txt`
- export TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER (ask a team member for the values, but dont put them in git)
- `createdb hack18`
- `python create_db.py`
- `python run.py` to run the Flask server
- Browse to `localhost:8080`!

- Make sure your phone number is verified at https://www.twilio.com/console/phone-numbers/verified (and you have to be invited to the project on Twilio for that link to work right) or the app will not be able to text you, in the trial stage.
