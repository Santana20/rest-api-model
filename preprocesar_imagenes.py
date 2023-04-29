import os
import time
from os import system
from PIL import Image
from predict_pose import generate_pose_keypoints
#from ACGPN.U-2-Net import u2net_load, u2net_run
cwd = os.getcwd()
os.chdir(os.getcwd() + '/U-2-Net/')
import u2net_load
import u2net_run
os.chdir(cwd)
os.getcwd()


def obtener_u2net():
    cwd = os.getcwd()
    os.chdir(os.getcwd() + '/U-2-Net/')
    u2net = u2net_load.model(model_name = 'u2netp')
    os.chdir(cwd)
    os.getcwd()
    return u2net

def preprocesar_ropa():
    # Ruta de la carpeta que contiene las imágenes de tela
    ruta_carpeta = '/content/ACGPN/inputs/cloth'

    # Obtener la lista de archivos en la carpeta y ordenarlos alfabéticamente
    archivos = sorted(os.listdir(ruta_carpeta))
    print(archivos)

    # Inicializar un contador para el número de la imagen
    num_imagen = 1

    u2net = obtener_u2net()
    for nombre_archivo in archivos:
        ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)
        if os.path.isfile(ruta_archivo):  # verifica que la ruta apunta a un archivo
            nombre_sin_extension, extension = os.path.splitext(nombre_archivo)
            nuevo_nombre_archivo = '{:06d}_1{}'.format(num_imagen, '.png')
            ruta_nuevo_archivo = os.path.join('/content/ACGPN/Data_preprocessing/test_color', nuevo_nombre_archivo)

            imagen = Image.open(ruta_archivo)
            imagen = imagen.resize((192, 256), Image.BICUBIC).convert('RGB')
            imagen.save(ruta_nuevo_archivo)
            
            cloth_path = os.path.join('/content/ACGPN/inputs/cloth', nombre_archivo)
            cloth = Image.open(cloth_path)
            cloth = cloth.resize((192, 256), Image.BICUBIC).convert('RGB')
            cloth.save(os.path.join('/content/ACGPN/Data_preprocessing/test_color', nuevo_nombre_archivo))
            u2net_run.infer(u2net, '/content/ACGPN/Data_preprocessing/test_color', '/content/ACGPN/Data_preprocessing/test_edge')

            num_imagen += 1

def preprocesar_img_user():
    start_time = time.time()
    
    img_dir = '/content/ACGPN/inputs/img'
    img_names = sorted([f for f in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, f)) and f.lower().endswith('.jpg') or f.lower().endswith('.jpeg') or f.lower().endswith('.png')])

    for i, img_name in enumerate(img_names):
        img_path = os.path.join(img_dir, img_name)
        img = Image.open(img_path)
        img = img.resize((192,256), Image.BICUBIC)

        new_img_name = '{:06d}_0.png'.format(i+1)
        img_path = os.path.join('/content/ACGPN/Data_preprocessing/test_img', new_img_name)
        img.save(img_path)

        print('Resized and saved image {} in {}s'.format(new_img_name, time.time()-start_time))
    
        #!python /content/ACGPN/Self-Correction-Human-Parsing-for-ACGPN/simple_extractor.py --dataset 'lip' --model-restore 'lip_final.pth' --input-dir '/content/ACGPN/Data_preprocessing/test_img' --output-dir '/content/ACGPN/Data_preprocessing/test_label'

        system("python /content/ACGPN/Self-Correction-Human-Parsing-for-ACGPN/simple_extractor.py --dataset 'lip' --model-restore 'lip_final.pth' --input-dir '/content/ACGPN/Data_preprocessing/test_img' --output-dir '/content/ACGPN/Data_preprocessing/test_label'")

        print('Parsing generated for image {} in {}s'.format(new_img_name, time.time()-start_time))

        pose_path = os.path.join('/content/ACGPN/Data_preprocessing/test_pose', new_img_name.replace('.png', '_keypoints.json'))
        generate_pose_keypoints(img_path, pose_path)

        print('Pose map generated for image {} in {}s'.format(new_img_name, time.time()-start_time))
