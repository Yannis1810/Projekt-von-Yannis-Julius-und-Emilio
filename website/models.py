from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import sqlite3
from flask_login import current_user
import datetime


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.cest.now()) #hier func.now(), falls es nicht funktioniert
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Fremdschlüssel


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') # Beziehung zu den Notizen
    repairs = db.relationship('Repair') # Beziehung zu den Reparaturen
    

class Repair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    r_object = db.Column(db.String(150))
    location = db.Column(db.String(1500))
    last_maintenance = db.Column(db.DateTime(timezone=True), default=func.now())
    tool = db.Column(db.String(150))
    next_maintenance = db.Column(db.String(1500))
    r_note = db.Column(db.String(10000))
    user_r_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class Trash(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(100), primary_key=True)
    plz = db.Column(db.String(5), primary_key=True)
    date = db.Column(db.Integer)
