#!/usr/bin/env python3
from flask import request, session
from flask_restful import Resource
from config import app, db, api
from models import *

class Signup(Resource):
  def post(self):
    user_request = request.get_json()
    name = user_request.get('name')
    username = user_request.get('username')
    password = user_request.get('password')

class Login(Resource):
  def post(self):
    pass

class CheckSession(Resource):
  def get(self):
    pass

class Logout(Resource):
  def delete(self):
    pass

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
api.add_resource(CheckSession, '/checksession')
api.add_resource(Logout, '/logout')
api.add_resource(UserIndex, '/users')
api.add_resource(Moods, '/moods/<id>')
