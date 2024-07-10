# save this as app.py
from flask import request, session, make_response, jsonify
from flask_restful import Resource
# from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Service

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

class ServiceList(Resource):
    def get(self):
        services = [service.to_dict() for service in Service.query.all()]
        return make_response(jsonify(services), 200)

api.add_resource(ServiceList, '/services')



if __name__ == '__main__':
    app.run(port=5555, debug=True)