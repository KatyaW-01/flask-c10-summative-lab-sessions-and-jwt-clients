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

class MoodIndex(Resource):
  #gets all of a users moods, paginated- cannot see other user's moods
  def get(self):
    user_id = session.get('user_id')
    if user_id:
      page = request.args.get("page", 1, type=int)
      per_page = request.args.get("per_page", 3, type=int)
      pagination = MoodTracker.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
      moods = pagination.items
      return {
        "page": page,
        "per_page": per_page,
        "total": pagination.total,
        "total_pages": pagination.pages,
        "moods": [MoodTrackerSchema().dump(mood) for mood in moods]
      }
    else:
      return {"error": "User not logged in"}, 401

  #create a new mood, assigned to the user that is logged in
  def post(self):
    if session.get('user_id'):
      request_json = request.get_json()
      user_mood = MoodTracker(
        mood = request_json.get('mood'),
        notes = request_json.get('notes'),
        user_id = session['user_id']
      )

      try:
        db.session.add(user_mood)
        db.session.commit()
        return MoodTrackerSchema().dump(user_mood), 201
      except IntegrityError:
        return {'error': '422 Unprocessable Entity'}, 422
    else:
      return {"error": "User not logged in"}, 401

class Moods(Resource):
  #get a single mood by id, can only view your own moods
  def get(self,id):
    if session.get('user_id'):
      user_mood = MoodTracker.query.filter_by(id=id, user_id=session['user_id']).first()
      if user_mood:
        return MoodTrackerSchema().dump(user_mood), 200
      else:
        return {'error': f'Mood {id} not found'}, 404
    else:
      return {"error": "User not logged in"}, 401
  
  #edit a mood, can only edit your own moods
  def patch(self, id):
    if session.get('user_id'):
      user_mood = MoodTracker.query.filter_by(id=id, user_id=session['user_id']).first()
      if user_mood:
        data = request.get_json()
        if 'mood' in data:
          user_mood.mood = data['mood']
        if 'notes' in data:
          user_mood.notes = data['notes']  
        
        db.session.commit()

        return {'message': f'mood {id} updated successfully'}, 200
      else:
        return {'error': f'Mood {id} not found'}, 404
    else:
      return {"error": "User not logged in"}, 401

  #delete a mood, can only delete your own moods
  def delete(self, id):
    if session.get('user_id'):
      mood = MoodTracker.query.filter_by(id=id, user_id=session['user_id']).first()
      if mood:
        db.session.delete(mood)
        db.session.commit()
        return {'message': f'Mood {id} for user {session.get('user_id')} deleted successfully'}, 200
      else:
        return {'error': f'Mood {id} not found'}, 404
    else:
      return {"error": "User not logged in"}, 401

api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Logout, '/logout')
api.add_resource(MoodIndex, '/moods')
api.add_resource(Moods, '/moods/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
