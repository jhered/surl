from flask import Flask, request ,jsonify, Response, redirect, url_for ,url_for, abort
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId
from string import digits, ascii_letters
from secrets import choice
from os import getenv

# seteamos la variable MONGO_URI de la variable de sistema MONGO_URI
MONGO_URI = getenv("MONGO_URI")

# seteamos longitud url_corta
max_redirect_len = 7
# url_corta puede armarse estos caracateres: 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
alphabet = digits + ascii_letters

app = Flask(__name__)

# utilizamos la variable MONGO_URI
app.config['MONGO_URI']= MONGO_URI

mongo = PyMongo(app)

redirects = mongo.db.acortador

@app.route('/crear', methods=['POST'])
def register_path():
    global max_redirect_len
    global redirects


    json_data = request.get_json()

    url_larga = None, None

    try:

        url_larga = json_data['url_larga']
    except:
        abort(500, description='Parametros invalidos Ej: "url_larga":"https://www.google.com.ar"')
    

# Verificar URL
    if url_larga[:7] != 'http://' and url_larga[:8] != 'https://':
        abort(400, description='URL Invalida Ej: "url_larga":"https://www.google.com.ar"')

# Verifica url existente
    redirect_existe = redirects.find_one({'url_larga':url_larga})

    if redirect_existe:
        return f'La URL  {url_larga} ya existe {redirect_existe["url_corta"]}'
    else:
        url_corta = ''.join([choice(alphabet) for i in range(max_redirect_len)])
        
        while redirects.find_one({'url_corta':url_corta}):
            url_corta = ''.join([choice(alphabet) for i in range(max_redirect_len)])

        redirects.insert_one({'url_corta':url_corta, 'url_larga':url_larga})

    return f'URL creada {url_larga} at /{url_corta}'

@app.route('/<path:path>', methods=['GET'])
def path_redirect(path):
    global redirects

    redirect_path = redirects.find_one({'url_corta': path})

    if not redirect_path:
        abort(404, description='No encontrada la URL')
    else:
        return redirect((redirect_path['url_larga']), code= 302)


@app.route('/borrar/<id>', methods=['DELETE'])
def delete_url_corta(id):

    mongo.db.acortador.delete_one({'url_corta': (id)})
    response = jsonify({'message': 'URL corta ' + id + ' fue borrada'})
    return response

@app.errorhandler(404)
def not_found(error=None):
        response = jsonify({
            'message': 'Recurso no encontrado: ' + request.url,
            'status': 404
        })
        response.status_code = 404
        return response    

# Configuracion del puerto para la app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080,debug=True)