import sys
import numpy as np
import trimesh
import matplotlib.pyplot as plt

from src.model_treatment import *

# import multiprocessing as mp
# pool = mp.Pool(mp.cpu_count())

"""
/distorsion longueur d'arrête + plot
Vérification du même nombre de point  
Texture
"""

# Path of models
args = ['../model/brain.ply',
        '../model/brain_sphere_1_iters.ply']
"""
        '../model/brain_sphere_2_iters.ply',
        '../model/brain_sphere_4_iters.ply',
        '../model/brain_sphere_8_iters.ply',
        '../model/brain_sphere_16_iters.ply',
        '../model/brain_sphere_32_iters.ply',
        '../model/brain_sphere_50_iters.ply',
        '../model/brain_sphere_75_iters.ply',
        '../model/brain_sphere_100_iters.ply',
        '../model/brain_sphere_200_iters.ply'
        ]"""

iters = [0,
         1,
         2,
         4,
         8,
         16,
         32,
         50,
         75,
         100,
         200
         ]


def main(argv):
    """
    if len(argv) >= 2:
    else:
        print("No ... you have to put model in var 'args'")
    """

    if len(args) >= 2:
        meshs = []
        for i in range(0, len(args)):
            print(args[i])
            mesh = trimesh.load(args[i])
            mesh.metadata = {'name': name_fil(args[i]), 'iters': iters[i]}
            meshs.append(mesh)

        # compare_mesh_list_angle(meshs)

        # compare_mesh_list_area(meshs)
        # compare_mesh_list_area_curve(meshs)
        compare_mesh_list_area_curve_pourcent(meshs)

        # display_plot()
        # display_model(meshs[1])
        # display_model(meshs[3])
        # superimpose_the_texture(meshs[0], meshs[1])
        # display_model(meshs[0])

    else:
        print("No ... you have to put path of model in var 'args' (min 2 models)")

    pass


def name_fil(path_file):
    path_file = str(path_file)
    name = ""
    for i in range(path_file.find("brain"), len(path_file)):
        name += (path_file[i])

    return name


def verification(mesh):
    pass


if __name__ == "__main__":
    main(sys.argv[1:])