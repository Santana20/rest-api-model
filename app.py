from flask import Flask, jsonify, request
from cloth import *
from descargar_imagen import descargar_img
from generar_tryon import generar_tryon
from flask_ngrok import run_with_ngrok

app  = Flask(__name__)
run_with_ngrok(app)

CLOTH_DIR = 'img/cloth/'
IMG_USER_DIR = 'img/user/'

@app.route('/')
def home():
    return 'Corriendo correctamente'

@app.route('/tryon', methods=['POST'])
def tryOn():
    request_data = request.get_json()
    # print(request_data)
    # guardamos la imagen de la ropa
    descargar_img(request_data['cloth']['url'], CLOTH_DIR)    
    # guardamos la imagen de la persona
    descargar_img(request_data['user']['url'], IMG_USER_DIR)

    # ejecutamos el test
    generar_tryon()    
    return request_data


if __name__ == '__main__':
    app.run()