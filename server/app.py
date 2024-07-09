# save this as app.py
from flask import request, session
from flask_restful import Resource
# from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User

@app.route('/')
def hello():
    return f'Hello there!'

class Login(Resource):
    def post(self):
        request_json = request.get_json()

        username = request_json.get('username')
        password = request_json.get('password')

        user = User.query.filter(User.username == username).first()

        if user:
            if user.authenticate(password):
                session['user_id'] = user.id
                return user.to_dict(), 200

        return {'error': '401 Unauthorized'}, 401

api.add_resource(Login, '/login', endpoint='login')