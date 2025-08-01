#!/usr/bin/env python3

from app import app
from models import *

with app.app_context():
  
  print("Deleting all records...")

  User.query.delete()
  MoodTracker.query.delete()

  print("Creating Users...")

  user1 = User(username="JoshK", password="password123",name="Josh")
  user2 = User(username="Mary1997", password="unicorns",name="Mary")
  user3 = User(username="TomSmith07",password="p123987", name="Tom")
  user4 = User(username="betty3", password="newpassword", name="Betty")
  user5 = User(username="MarkW", password="firetruck", name="Mark")

  db.session.add_all([user1,user2,user3,user4,user5])
  
  print("Creating User's moods...")

  mood1 = MoodTracker(mood="happy", notes="I had a really great day today.", user = user1.id)
  mood2 = MoodTracker(mood="excited", notes="Leaving for vacation today!", user = user2.id)
  mood3 = MoodTracker(mood="frustrated", notes="My boss won't give me a promotion.", user = user3.id)
  mood4 = MoodTracker(mood="sad", notes="My best friend lives far away from me and I dont get to see her very often.", user = user4.id)
  mood5 = MoodTracker(mood="bored", notes="I finished my work early and don't have anything to do.", user = user5.id)

  db.session.add_all([mood1,mood2,mood3,mood4,mood5])

  db.session.commit()

  print("Complete.")