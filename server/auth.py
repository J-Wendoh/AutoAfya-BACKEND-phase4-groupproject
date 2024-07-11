from flask import Blueprint, jsonify, make_response
from flask_restful import Api, Resource, reqparse
from models import User, db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, JWTManager, create_refresh_token, jwt_required, current_user, get_jwt
from functools import wraps

JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')
bcrypt = Bcrypt()
jwt = JWTManager()
auth_api = Api(auth_bp)
BLACKLIST = set()


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in BLACKLIST


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).first()


register_args = reqparse.RequestParser()
register_args.add_argument('email')
register_args.add_argument('password')
register_args.add_argument('username')


login_args = reqparse.RequestParser()
login_args.add_argument('email')
login_args.add_argument('password')

class Register(Resource):

    def post(self):

        data = register_args.parse_args()
        hashed_password = bcrypt.generate_password_hash(data.get('password'))
        new_user = User(email=data.get('email'), username=data.get(
            'username'), password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return {"msg": 'user created successfully'}

class Login(Resource):

    def post(self):
        data = login_args.parse_args()
        # check if the user exists in our db
        user = User.query.filter_by(email=data.get('email')).first()
        if not user:
            return {"msg": "User Does not exists in our DataBase"}
        if not bcrypt.check_password_hash(user.password, data.get('password')):
            return {"msg": "Password is incorrect!"}
        # check if the password is correct

        # login
        token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return {"token": token, "refresh_token": refresh_token}

    @jwt_required(refresh=True)
    def get(self):
        token = create_access_token(identity= current_user.id )
        return {"token":token}


class Logout(Resource):

    @jwt_required()
    def post(self):
        # Get the JWT token's JTI (unique identifier)
        jti = get_jwt()['jti']

        # Add the JTI to the blacklist
        BLACKLIST.add(jti)

        return make_response(jsonify({'message': 'Successfully logged out'}), 200)


# routes
auth_api.add_resource(Register, '/register')
auth_api.add_resource(Login, '/login')
auth_api.add_resource(Logout, '/logout')