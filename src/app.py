"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints

npm run start (en una terminal) este se abre en el frontend y es el 3000
-3001 va  a estar el backend (que debemos convertir en publico)
pipenv run start

Esto es para generar el token 
pipenv install flask-jwt-extended

En el .env tambien podemos guardar el link del puerto 3001 

BACKEND_URL = gitpod.. 

La llave super secreta tenemos que guardarla en nuestro archivo .env tambien:

JWT_KEY = "super-secret"

Postman: 
Authorization
Y despues "Bearer Token"
"""
import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger
from api.utils import APIException, generate_sitemap
from api.models import db
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands
from api.models import db, User
from flask_cors import CORS 

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
# from models import Person

ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '../public/')
app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app) 
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_KEY")
jwt = JWTManager(app)       

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
#LOGIN: 
@app.route('/login', methods=['POST'])
def login():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar informacion '}), 400
    if 'email'  not in body:
        return jsonify({'msg': 'El campo email es obligatorio'}), 400
    if 'password' not in body:
        return jsonify({'msg': 'El campo password es obligatorio'}), 400
    user = User.query.filter_by(email=body['email']).first()
    if user is None:
        return jsonify({'msg': "email is invalid"}), 400
    if user.password != body['password']:
        return jsonify({'msg': "password is invalid"}), 400
    access_token = create_access_token(identity=user.email) #se le pone algo que se pueda identificar como en este caso el mail
    return jsonify({'msg': 'ok', 'token': access_token}), 200 #ese access_token se puede ver en postman y se puede ir a la pagina https://jwt.io/ para verlo


#Restringir acceso a paginas si no es usuario
@app.route('/private', methods=['GET'])
@jwt_required()
def private():
    current_user = get_jwt_identity()
    print('Este es el usuario que esta haciendo la peticion: ', current_user)
    return jsonify({'msg': 'Bienvenido', 'Este es el usuario que esta haciendo la peticion: ': current_user})
    

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)
