import os
from os import system

def changeDir():
    cwd = os.getcwd()
    os.chdir(os.getcwd() + '/U-2-Net/')
    os.chdir(cwd)
    os.getcwd()

list_of_commands = [
    #'pip install ninja',
    'mkdir ACGPN/Data_preprocessing/test_color',
    'mkdir ACGPN/Data_preprocessing/test_colormask',
    'mkdir ACGPN/Data_preprocessing/test_edge',
    'mkdir ACGPN/Data_preprocessing/test_img',
    'mkdir ACGPN/Data_preprocessing/test_label',
    'mkdir ACGPN/Data_preprocessing/test_mask',
    'mkdir ACGPN/Data_preprocessing/test_pose',
    'mkdir ACGPN/inputs',
    'mkdir ACGPN/inputs/img',
    'mkdir ACGPN/inputs/cloth',
    'mkdir ACGPN/saved_models',
    'mkdir ACGPN/saved_models/u2net',
    'mkdir ACGPN/saved_models/u2netp',
    'mkdir ACGPN/checkpoints',
]

for command in list_of_commands:
    system(command)

