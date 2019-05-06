import sys
import numpy as np
import trimesh
import matplotlib.pyplot as plt

from src.model_treatment import *

# import multiprocessing as mp
# pool = mp.Pool(mp.cpu_count())

"""
# arg à la dure (pour le main) / les commentaires / nom fonctions / histogramme +de la différence d'aire en fonction du nombre d'iters du model
/distorsion longueur d'arrête + plot
echantillonage 1 2 4 8 16 32 50 75 100 iters model
"""

def main(argv):
    if len(argv) >= 2:
        meshs = []
        for i in range(0, len(argv)):
            print(argv[i])
            mesh = trimesh.load(argv[i])
            mesh.metadata = {'name' : argv[i]}
            meshs.append(mesh)

        compare_mesh_list_angle(meshs)
        compare_mesh_list_area(meshs)

        #display_plot()
        # display_model(meshs[1])
        # display_model(meshs[3])
        superimpose_the_texture(meshs[0], meshs[1])
        display_model(meshs[0])
    else:
        print("Non")
    pass


if __name__ == "__main__":
    main(sys.argv[1:])

""" Texture """
