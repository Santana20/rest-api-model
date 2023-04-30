import requests
def descargar_img(url_img, localDir='img/'):
    nombre_img_local = url_img.split('/')[-1]
    if not nombre_img_local:
        nombre_img_local = 'prueba.jpg'
    imagen = requests.get(url_img).content
    with open(f'{localDir}{nombre_img_local}', 'wb') as handler:
        handler.write(imagen)
