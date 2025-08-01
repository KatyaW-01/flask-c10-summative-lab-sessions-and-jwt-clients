from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from marshmallow import Schema, fields
from sqlalchemy.ext.hybrid import hybrid_property

from config import db, bcrypt

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String, unique=True, nullable = False)
  _password_hash = db.Column(db.String)
  name = db.Column(db.String, nullable=False)

  mood = db.relationship('MoodTracker', back_populates='user')

  @hybrid_property
  def password_hash(self):
    raise AttributeError('Passwords may not be viewed')
  
  @password_hash.setter
  def password_hash(self,password):
    password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
    self._password_hash = password_hash.decode('utf-8')

  def authenticate(self,password):
    return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

  def __repr__(self):
    return f"<User {self.id}, {self.name}>"
  
class UserSchema(Schema):
  id = fields.Int(dump_only=True)
  username = fields.String()
  name = fields.String()
  mood = fields.Nested(lambda: UserSchema(exclude=("user",)))

class MoodTracker(db.Model):
  __tablename__ = 'mood_tracker'

  id = db.Column(db.Integer, primary_key=True)
  mood = db.Column(db.String, nullable=False)
  notes = db.Column(db.String, nullable=False)

  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  user = db.relationship('User', back_populates='mood')

  def __repr__(self):
    return f"<Mood {self.id}, {self.mood}, {self.notes}>"

class MoodTrackerSchema(Schema):
  id = fields.Int(dump_only=True)
  mood = fields.String()
  notes = fields.String()
  user = fields.Nested(lambda: UserSchema(exclude=("mood",)))

