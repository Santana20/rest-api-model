from flask import Flask, jsonify, request, send_file

import os
from os import system
cwd = os.getcwd()
os.chdir(os.getcwd() + '/rest-api-model/')
from descargar_imagen import descargar_img
import preprocesar_imagenes as prepro
os.chdir(cwd)
os.getcwd()


REST_DIR = 'rest-api-model/'
CLOTH_DIR = REST_DIR +'img/cloth/'
IMG_USER_DIR = REST_DIR + 'img/user/'


def guardar_resultado():
    system(f'cp ./ACGPN/results/test/try-on/* {REST_DIR}img/result/')

def generar_tryon():
    # Movemos las imagenes al directorio
    system(f"cp {REST_DIR}img/cloth/* ../ACGPN/inputs/cloth/")
    system(f"cp {REST_DIR}img/user/* ../ACGPN/inputs/img/")
    
    prepro.preprocesar_ropa()
    prepro.preprocesar_img_user()
    prepro.generar_test_pair_txt()

    guardar_resultado()

from flask_ngrok import run_with_ngrok

app  = Flask(__name__)
run_with_ngrok(app)


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
  # generar_tryon()

  # Movemos las imagenes al directorio
  print('copiamos las imagenes recibidas')
  system(f"cp {REST_DIR}img/cloth/* ACGPN/inputs/cloth/")
  system(f"cp {REST_DIR}img/user/* ACGPN/inputs/img/")
  
  print('Preprocesamos la ropa')
  prepro.preprocesar_ropa()
  print('Preprocesamos la imagen user')
  prepro.preprocesar_img_user()
  print('Generamos archivo test_pair')
  prepro.generar_test_pair_txt()

  print("ejecutar archivo test.py de ACGPN")
  prepro.correr_test_tryon()

  print('Copiamos el resutado acgpn al rest')
  filename = f'{REST_DIR}img/result/000001_0.png'
  system(f'cp ./ACGPN/results/test/try-on/* {REST_DIR}img/result/')

  print('eliminamos las imagenes en ACGPN para nuevo test')
  list_rm = [
      'rm -rf ACGPN/Data_preprocessing/test_color/*',
      'rm -rf ACGPN/Data_preprocessing/test_colormask/*',
      'rm -rf ACGPN/Data_preprocessing/test_edge/*',
      'rm -rf ACGPN/Data_preprocessing/test_img/*',
      'rm -rf ACGPN/Data_preprocessing/test_label/*',
      'rm -rf ACGPN/Data_preprocessing/test_mask/*',
      'rm -rf ACGPN/Data_preprocessing/test_pose/*',
      'rm -rf ACGPN/inputs/cloth/*',
      'rm -rf ACGPN/inputs/img/*',
      'rm -rf ACGPN/results/*',
      'rm -rf rest-api-model/img/cloth/*',
      'rm -rf rest-api-model/img/user/*'
  ]

  for command in list_rm:
    system(command)

  return send_file(filename, mimetype='image/x-png')


if __name__ == '__main__':
    app.run()