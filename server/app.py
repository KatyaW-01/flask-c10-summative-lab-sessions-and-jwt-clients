#!/usr/bin/env python3
from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from config import app, db, api
from models import User, UserSchema, MoodTracker, MoodTrackerSchema

class Signup(Resource):
  def post(self):
    user_request = request.get_json()
    name = user_request.get('name')
    username = user_request.get('username')
    password = user_request.get('password')
    user = User(username=username, name=name)
    user.password_hash = password
    try:
      db.session.add(user)
      db.session.commit()
      session['user_id'] = user.id
      return UserSchema().dump(user), 201
    except IntegrityError as e:
      print("IntegrityError:", e)
      return {'error': '422 Unprocessable Entity'}, 422

class Login(Resource):
  def post(self):
    username = request.get_json()['username']
    password = request.get_json()['password']
    
    user = User.query.filter(User.username == username).first()

    if user and user.authenticate(password):
      session['user_id'] = user.id
      return UserSchema().dump(user), 200
    
    return {'error': '401 Unauthorized'}, 401

class CheckSession(Resource):
  def get(self):
    if session.get('user_id'):
      user = User.query.filter(User.id == session['user_id']).first()
      return UserSchema().dump(user), 200
    else:
      return {"error": "User is not logged in"}, 401

class Logout(Resource):
  def delete(self):
    if session.get('user_id'):
      session['user_id'] = None
      return {}, 204
    return {"error": "User is already logged out" }, 401

class UserIndex(Resource):
  def get(self):
    #get all users and associated moods
    #paginated
    pass

  def post(self):
    #create a mood
    pass

class Moods(Resource):

  def patch(self):
    #update a mood
    pass

  def delete(self):
    #delete a mood
    pass

api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Logout, '/logout')
api.add_resource(UserIndex, '/users')
api.add_resource(Moods, '/moods/<id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
