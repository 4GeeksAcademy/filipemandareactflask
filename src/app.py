"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger
from api.utils import APIException, generate_sitemap
from api.models import db, Todolist , User
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands
from flask_cors import CORS

# from models import Person

ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '../public/')

app = Flask(__name__)
app.url_map.strict_slashes = False

# database condiguration
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db, compare_type=True)
db.init_app(app)

# Allow CORS requests to this API
CORS(app)

# add the admin
setup_admin(app)

# add the admin
setup_commands(app)

# Add all endpoints form the API with a "api" prefix
app.register_blueprint(api, url_prefix='/api')

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    if ENV == "development":
        return generate_sitemap(app)
    return send_from_directory(static_file_dir, 'index.html')

# any other endpoint will try to serve it like a static file


@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0  # avoid cache memory
    return response



@app.route('/todos', methods=['GET'])
def get_task():
    all_tasks = Todolist.query.all()
    response_body = list(map(lambda x: x.serialize(), all_tasks))
    return jsonify(response_body), 200


@app.route('/todos', methods=['POST'])
def post_task():
    new_task = request.json
    task = Todolist(task =new_task['task'], done =new_task['done'])
    db.session.add(task)
    db.session.commit() 

    all_tasks = Todolist.query.all()
    response_body = list(map(lambda x: x.serialize(), all_tasks))
    return jsonify(response_body), 200



@app.route('/todos/<id>', methods=['PUT'])
def update_task(id):
    new_task = request.json
    update_task = Todolist.query.get(id)
    update_task.done = new_task['done'] 
    db.session.commit()

    all_tasks = Todolist.query.all()
    response_body = list(map(lambda x: x.serialize(), all_tasks))
    return jsonify(response_body), 200

@app.route('/todos/<id>', methods=['DELETE'])
def delete_task(id):
    del_task = Todolist.query.get(id)
    db.session.delete(del_task)
    db.session.commit()

    return jsonify(f'delete'), 200


@app.route('/user', methods=['POST'])
def create_user():
    new_user = request.json
    user = User(email =new_user['email'], password =new_user['password'])
    db.session.add(user)
    db.session.commit() 

    all_user = User.query.all()
    response_body = list(map(lambda x: x.serialize(), all_user))
    return jsonify(response_body), 200


@app.route('/user', methods=['GET'])
def get_user():
    all_users = User.query.all()
    response_body = list(map(lambda x: x.serialize(), all_users))
    return jsonify(response_body), 200

@app.route('/login', methods=['POST'])
def login():
    new_user = request.json
    user =  User.query.filter_by(email=new_user["email"]).first()
    if user.password == new_user["password"]:
    
        return jsonify(user.serialize()), 200

    else :
        
        return "password does not match" , 400








# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)
