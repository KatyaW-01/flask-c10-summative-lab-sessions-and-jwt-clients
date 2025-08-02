#!/usr/bin/env python3

from config import app
from models import db, User, MoodTracker

with app.app_context():
  
  print("Deleting all records...")

  User.query.delete()
  MoodTracker.query.delete()

  print("Creating Users...")

  user1 = User(username="JoshK",name="Josh")
  user1.password_hash = "password123"
  user2 = User(username="Mary1997",name="Mary")
  user2.password_hash = "unicorns"
  user3 = User(username="TomSmith07", name="Tom")
  user3.password_hash = "p123987"
  user4 = User(username="betty3", name="Betty")
  user4.password_hash = "newpassword"
  user5 = User(username="MarkW", name="Mark")
  user5.password_hash = "firetruck"

  db.session.add_all([user1,user2,user3,user4,user5])
  db.session.commit()
  
  print("Creating User's moods...")

  mood1 = MoodTracker(mood="happy", notes="I had a really great day today.", user_id = user1.id)
  mood2 = MoodTracker(mood="excited", notes="Leaving for vacation today!", user_id = user2.id)
  mood3 = MoodTracker(mood="frustrated", notes="My boss won't give me a promotion.", user_id = user3.id)
  mood4 = MoodTracker(mood="sad", notes="My best friend lives far away from me and I dont get to see her very often.", user_id = user4.id)
  mood5 = MoodTracker(mood="bored", notes="I finished my work early and don't have anything to do.", user_id = user5.id)

  db.session.add_all([mood1,mood2,mood3,mood4,mood5])

  db.session.commit()

  print("Complete.")