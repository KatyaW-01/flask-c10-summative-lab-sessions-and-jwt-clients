from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from marshmallow import Schema, fields

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)

  mood = db.relationship('MoodTracker', back_populates='user')

  def __repr__(self):
    return f"<User {self.id}, {self.name}>"
  
class UserSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.String()

  mood = fields.Nested(lambda: UserSchema(exclude=("user",)))

class MoodTracker(db.Model):
  __tablename__ = 'mood_tracker'

  id = db.Column(db.Integer, primary_key=True)
  mood = db.Column(db.String, nullable=False)
  notes = db.Column(db.String, nullable=False)

  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  user = db.relationship('User', back_populates='mood')

class MoodTrackerSchema(Schema):
  id = fields.Int(dump_only=True)
  mood = fields.String()
  notes = fields.String()

  user = fields.Nested(lambda: UserSchema(exclude=("mood",)))

