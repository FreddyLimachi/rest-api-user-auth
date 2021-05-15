
from flask import request, jsonify
from pymongo import MongoClient
from flask_jwt_extended import jwt_required, create_access_token, get_raw_jwt, verify_jwt_in_request
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

from datetime import timedelta
from .validators import validate

load_dotenv() # Inicializando las variables de entorno

# Definiendo la conexion a MongoDB
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client['my_db'] # base de datos
collection = db['users'] # collecion

# definiendo una lista para almacenar tokens de cierre de sesión
blacklist = set()

def create_user():

    try:
        verify_jwt_in_request()
        return jsonify({'msg':'Error, ya esta logeado'}), 404
    except: pass

    # Obteniendo el nombre de usuario sin espacios al inicio y final
    try:
        username = request.json['username'].strip()
        email = request.json['email']
        password = request.json['password']
        confirm_pass = request.json['confirm_pass']
        
    except TypeError: return jsonify({'msg': 'Enviar en formato JSON'}), 400
    except KeyError: return jsonify({'msg': 'Complete todos los datos'}), 400
        

    user = collection.find_one({'username': {'$regex': username, '$options': 'i'}})
    verify_email = collection.find_one({'email': {'$regex': email, '$options': 'i'}})

    val = validate(username, email, password, confirm_pass, user, verify_email) # validar datos
    if val != True: return jsonify(val)
    
    password_hash = generate_password_hash(password)

    id = collection.insert({
        'username': username,
        'email': email,
        'password': password_hash
    })

    expires = timedelta(days=30)
    access_token = create_access_token(identity = username, expires_delta = expires)
    return jsonify({'value': True, 'access_token': access_token}), 200


def authenticate():
    try:
        verify_jwt_in_request()
        return jsonify({'msg':'Error, ya esta logeado'}), 404
    except: pass
    
    #obteniendo el nombre de usuario sin espacios al inicio y final
    username = request.json['username'].strip() 
    password = request.json['password']

    user = collection.find_one({'username': username})

    try: check_password = check_password_hash(user['password'], password)
    except TypeError: return jsonify(access_token = None), 401

    if check_password: 
        expires = timedelta(days=30)
        access_token = create_access_token(identity = username, expires_delta = expires)
        return jsonify(access_token = access_token), 200

    else: return jsonify(access_token = None), 401


@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200

