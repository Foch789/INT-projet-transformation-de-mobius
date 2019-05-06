import sys
import numpy as np
import trimesh
import matplotlib.pyplot as plt

import slam.plot as splt

from src.model_treatment import *


def use_exe():
    print("Utilisation du programme")
    pass


# import multiprocessing as mp
# pool = mp.Pool(mp.cpu_count())


def main(argv):

    if len(argv) >= 2:
        meshs = []

        for i in range(0, len(argv)):
            print(argv[i])
            meshs.append(argv[i])
            meshs.append(trimesh.load(argv[i]))

        mesh_angle(meshs)
        mesh_area(meshs)

        display_plot()
        # display_model(meshs[1])
        # display_model(meshs[3])
        superimpose_the_texture(meshs[1], meshs[3])
        # display_model(meshs[1])

    elif len(argv) == 1:
        print("Non")
    else:
        use_exe()
    pass


if __name__ == "__main__":
    main(sys.argv[1:])
