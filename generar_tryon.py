from os import system
import preprocesar_imagenes as prepro

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