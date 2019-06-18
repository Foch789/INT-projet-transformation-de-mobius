"""@package docstring
Documentation for this module.
More details.
"""

import numpy as np
import matplotlib.pyplot as plt

import slam.distortion as dist


"""
=====================================================
======================= Angle =======================
=====================================================
"""

def compare_mesh_list_angle(meshs):
    """
        Compare_mesh_list_angle

        Compare all models by their angles with
        the first model to see the distortion (first trismesh of array).
        !!! Use display_plot() for the display of result AND IT'S NOT NORMALIZING !!!
        (display a histogram)

        :param meshs
        :type array [trimesh,trimesh,...]
    """

    mesh1 = meshs[0]
    for i in range(1, len(meshs)):
        angle_diff = dist.angle_difference(mesh1, meshs[i])
        f, ax = plt.subplots(1, 1)
        ax.set_title('angles compare '
                     + mesh1.metadata['name']
                     + " to "
                     + meshs[i].metadata['name'])
        ax.hist(angle_diff.flatten(), 100)
        ax.grid(True)

    pass


def compare_mesh_list_angle_pourcent(meshs):
    """
        compare_mesh_list_area_curve_pourcent

        Compare all models by their areas with
        the first model to see the distortion in pourcent (first trismesh of array).
        !!! Use display_plot() for the display of result !!!
        (Display a curve)

        :param meshs
        :type array [trimesh,trimesh,...]
    """

    mesh1 = meshs[0]
    array_name = []
    array_result = []

    for i in range(1, len(meshs)):
        result = abs((meshs[i].face_angles/np.sum(meshs[i].face_angles))
                     - (mesh1.face_angles/np.sum(mesh1.face_angles)))
        result_result = np.sum(result) * 100
        array_name.append(i)
        array_result.append(result_result)

    names = array_name
    values = array_result

    fig2, ax2 = plt.subplots(1, 1)
    ax2.plot(names, values, 'ro-')
    ax2.set_title('Angles compare in pourcent curve')
    ax2.set_xlabel('Model to compare')
    ax2.set_ylabel('Angles compare in pourcent')

    print("Average of distortion in pourcent (Angles): "
          + str(np.sum(array_result)/len(array_result))
          + "%")

    return np.sum(array_result) / len(array_result), values
    pass


"""
=====================================================
======================= Area ========================
=====================================================
"""


def compare_mesh_list_area(meshs):
    """
        Compare_mesh_angle

        Compare all models by their areas with
        the first model to see the distortion (first trismesh of array).
        !!! Use display_plot() for the display of result AND IT'S NOT NORMALIZING !!!
        (display a histogram)

        :param meshs
        :type array [trimesh,trimesh,...]
    """

    mesh1 = meshs[0]
    for i in range(1, len(meshs)):
        area_diff = dist.area_difference(mesh1, meshs[i])
        f, ax = plt.subplots(1, 1)
        ax.set_title('areas compare '
                     + mesh1.metadata['name']
                     + " to "
                     + meshs[i].metadata['name'])
        ax.hist(area_diff.flatten(), 100)
        ax.grid(True)

    pass


def compare_mesh_list_area_pourcent(meshs):
    """
        compare_mesh_list_area_curve_pourcent

        Compare all models by their areas with
        the first model to see the distortion in pourcent in pourcent (first trismesh of array).
        !!! Use display_plot() for the display of result !!!
        (Display a curve)

        :param meshs
        :type array [trimesh,trimesh,...]
    """

    mesh1 = meshs[0]
    array_name = []
    array_result = []

    for i in range(1, len(meshs)):
        result = abs((meshs[i].area_faces/meshs[i].area)
                     - (mesh1.area_faces/mesh1.area))
        result_result = np.sum(result) * 100
        array_name.append(i)
        array_result.append(result_result)

    names = array_name
    values = array_result

    fig2, ax2 = plt.subplots(1, 1)
    ax2.plot(names, values, 'ro-')
    ax2.set_title('Areas compare in pourcent curve')
    ax2.set_xlabel('Model to compare')
    ax2.set_ylabel('Areas compare in pourcent')

    print("Average of distortion in pourcent (Areas): "
          + str(np.sum(array_result)/len(array_result))
          + "%")

    return np.sum(array_result) / len(array_result), values
    pass


"""
============================================================
======================= Edge length ========================
============================================================
"""


def compare_mesh_list_edge_pourcent(meshs):
    """
        compare_mesh_list_edge_pourcent

        Compare all models by their edges with
        the first model to see the distortion in pourcent (first trismesh of array)
        !!! Use display_plot() for the display of result !!!
        (Display a curve)

        :param meshs
        :type array [trimesh,trimesh,...]
    """
    mesh1 = meshs[0]
    array_name = []
    array_result = []
    for i in range(1, len(meshs)):
        result = abs((meshs[i].edges_unique_length
                      / np.sum(meshs[i].edges_unique_length))
                     - (mesh1.edges_unique_length
                        / np.sum(mesh1.edges_unique_length)))
        result_result = np.sum(result) * 100
        array_name.append(i)
        array_result.append(result_result)

    names = array_name
    values = array_result

    fig2, ax2 = plt.subplots(1, 1)
    ax2.plot(names, values, 'ro-')
    ax2.set_title('Edges compare in pourcent curve')
    ax2.set_xlabel('Model to compare')
    ax2.set_ylabel('Edges compare in pourcent')

    print("Average of distortion in pourcent (Edges length): "
          + str(np.sum(array_result) / len(array_result))
          + "%")

    return np.sum(array_result) / len(array_result), values
    pass


"""
========================================================================
======================= Superimpose the texture ========================
========================================================================
"""


def superimpose_the_texture(mesh1, mesh2):
    """
        superimpose_the_texture

        Take the texture of mesh2 and superimpose on the mesh1

        :param mesh1
        :type trimesh

        :param mesh2
        :type trimesh

        :return new mesh1 with texture
    """

    mesh_copy = mesh1.copy()
    mesh_copy.visual.face_colors = mesh2.visual.face_colors

    return mesh_copy

    pass
