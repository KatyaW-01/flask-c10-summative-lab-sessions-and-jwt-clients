#!/usr/bin/env python3

from app import app
from models import *

with app.app_context():
  
  print("Deleting all records...")

  User.query.delete()
  MoodTracker.query.delete()

  print("Creating Users...")
  user1 = User(name="Josh")
  user2 = User(name="Mary")
  user3 = User(name="Tom")
  user4 = User(name="Mark")
  user5 = User(name="Betty")

  db.session.add_all([user1,user2,user3,user4,user5])

  print("Creating User's moods...")