import os
from os import system
cwd = os.getcwd()
os.chdir(os.getcwd() + '/rest-api-model/')
import preprocesar_imagenes as prepro
os.chdir(cwd)
os.getcwd()

def guardar_resultado():
    system('cp ../ACGPN/results/test/try-on/* img/result/')

def generar_tryon():
    # Movemos las imagenes al directorio
    system("cp img/cloth/* ../ACGPN/inputs/cloth/")
    system("cp img/user/* ../ACGPN/inputs/img/")
    
    prepro.preprocesar_ropa()
    prepro.preprocesar_img_user()
    prepro.generar_test_pair_txt()

    guardar_resultado()