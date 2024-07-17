# save this as app.py

from flask import Flask, request, session, make_response, jsonify
from flask_migrate import Migrate
from auth import auth_bp, bcrypt, jwt
from customer import customer_bp
from models import db, User, Service
from flask_cors import CORS
# from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.secret_key = b'63969f31642049b6867473ddf8e3ff5e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://auto_afya_database_user:sMLKPChjBlh0zgGMCxkS8cFSFolr089c@dpg-cqbee3dds78s73aajb40-a.oregon-postgres.render.com/auto_afya_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

app.register_blueprint(customer_bp)
app.register_blueprint(auth_bp)
CORS(app,)

bcrypt.init_app(app)
db.init_app(app)
jwt.init_app(app)
migrate = Migrate(app=app, db=db)



@app.route('/')
def hello():
    return f'Hello there!'

if __name__ == '__main__':
    app.run(port=5555, debug=True)