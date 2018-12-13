from datetime import datetime
from random import randint

from sqlalchemy.orm import validates

from app.db import DB
from app.utils import normalize_number


class User(DB.Model):
    __tablename__ = "users"

    id = DB.Column(DB.Integer, primary_key=True)
    phone_number = DB.Column(DB.Text, nullable=False, unique=True)
    confirmed = DB.Column(DB.Boolean, nullable=False, default=False)
    last_active = DB.Column(DB.DateTime)

    @validates("phone_number")
    def validate_phone_number(self, _, phone_number):
        return normalize_number(phone_number)

class Response(DB.Model):
    __tablename__ = "responses"

    id = DB.Column(DB.Integer, primary_key=True)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('users.id'))
    raw = DB.Column(DB.Text, nullable=False)
    happiness = DB.Column(DB.Integer)
    timestamp = DB.Column(DB.DateTime, nullable=False, default=datetime.utcnow)

def seed_test_data():
    ''' Seed test data '''
    
    good_events = [
        'hot date',
        'walk on the beach',
        'bike ride',
        'my team won',
        'bought a new car',
        'got married',
        'bought a new house',
        'ate ice cream',
        'went mountain biking',
        'went surfing',
        'brushed my teeth',
        'ate a well-marbled steak',
        "slashed my ex's tires",
        'won the lottery',
        'won a used car',
        'won a used plane',
        'became dictator of a country',
        'got a hug',
        'went shopping',
        'read a book',
        'drank water',
        'left my awful job',
        'watched south park',
        'proved the existence of manbearpig',
        "didn't have to use my AK"
    ]

    bad_events = [
        'stepped in gum',
        'flaming turd dropped in front of house',
        'broke up with partner',
        'my team lost',
        'got divorced',
        'car was reposessed',
        'house burned down',
        'contracted mono'
    ]

    test_numbers = []

    for i in range(0, 3):
        user = User(
            phone_number=str(randint(10000000000, 99999999999)),
            confirmed=True
        )
        DB.session.add(user)
        DB.session.commit()

        test_numbers.append(user.id)

        for i in range(0, 50):
            happiness = randint(0, 5)
            event = ''
            if (happiness < 3):
                event = bad_events[randint(0, len(bad_events) - 1)]
            else:
                event = good_events[randint(0, len(bad_events) - 1)]

            DB.session.add(Response(
                user_id = user.id,
                raw = event,
                happiness=happiness
            ))

    DB.session.commit()
    return test_numbers

