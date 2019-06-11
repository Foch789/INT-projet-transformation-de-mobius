import numpy as np
import matplotlib.pyplot as plt

import slam.distortion as dist
import slam.plot as splt



def vertex_color_sphere(mesh):
    """
    Visualize a trimesh object using pyglet as proposed in trimesh
    the added value is for texture visualization
    :param mesh: trimesh object
    :return mesh wth :
    """

    meshC = mesh.copy()

    splt.pyglet_plot(meshC, meshC.vertices[:, 2])

    return meshC


def mobius_transformation(a, b, c, d, array_complex):

    # print(array_complex)

    numerator = (a * array_complex) + b
    denominator = (c * array_complex) + d

    result = numerator / denominator

    return result
