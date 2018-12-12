from datetime import datetime

from db import DB

class User(DB.Model):
    __tablename__ = "users"

    id = DB.Column(DB.Integer, primary_key=True)
    phone_number = DB.Column(DB.Text, nullable=False, unique=True)
    last_active = DB.Column(DB.DateTime)
    confirmed = DB.Column(DB.Bool)

class Response(DB.Model):
    __tablename__ = "responses"

    id = DB.Column(DB.Integer, primary_key=True)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('users.id'))
    raw = DB.Column(DB.Text, nullable=False)
    happiness = DB.Column(DB.Integer)
    timestamp = DB.Column(DB.DateTime, nullable=False, default=datetime.utcnow)
