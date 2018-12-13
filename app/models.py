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
    
    events = [
        'hot date',
        'walk on the beach',
        'bike ride',
        'my team won',
        'my team lost',
        'got divorced',
        'bought a new car',
        'car was reposessed',
        'house burned down',
        'got married',
        'broke up with partner',
        'bought a new house',
        'ate ice cream',
        'went mountain biking',
        'went surfing',
        'brushed my teeth',
        'ate a well-marbled steak',
        'stepped in gum',
        'flaming turd dropped in front of house',
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
        'proved the existence of manbearpig'
    ]

    for i in range(0, 10):
        user = User(
            phone_number=randint(10000000000, 99999999999),
            confirmed=True
        )
        DB.session.add(user)

        for i in range(0, 50):
            DB.session.add(Response(user.id,
                raw = events[randint(0, len(events - 1))],
                happiness=randint(0, 5)
            ))

    DB.session.commit()

