"""@package docstring
Documentation for this module.
More details.
"""

import numpy as np
import matplotlib.pyplot as plt

import slam.distortion as dist
import slam.plot as splt

# =====================================================
# ======================= Angle =======================
# =====================================================


def compare_mesh_list_angle(meshs):
    """
        Compare_mesh_list_angle

        Compare all models by their angles with
        the first model (first trismesh of array).
        !!! Use display_plot() for the display of result !!!
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
        the first model in pourcent (first trismesh of array).
        !!! Use display_plot() for the display of result !!!
        (One display with histogram and one other with curve)

        :param meshs
        :type array [trimesh,trimesh,...]
    """

    mesh1 = meshs[0]
    array_result = []

    for i in range(1, len(meshs)):
        result = abs((meshs[i].face_angles/np.sum(meshs[i].face_angles))
                     - (mesh1.face_angles/np.sum(mesh1.face_angles)))
        result_result = np.sum(result) * 100
        print(result_result)
        array_result.append(result_result)

    names = [(meshs[i].metadata['iters']) for i in range(1, len(meshs))]
    values = array_result

    # fig, ax = plt.subplots(1, 1)
    # plt.bar(names, values)
    # ax.set_title('Angles compare in pourcent')
    # ax.set_xlabel('Iterations')
    # ax.set_ylabel(' % difference angles')

    fig2, ax2 = plt.subplots(1, 1)
    ax2.plot(names, values, 'ro-')
    ax2.set_title('Angles compare in pourcent curve')
    ax2.set_xlabel('Iterations')
    ax2.set_ylabel('Areas compare in pourcent')

    print("Average of distortion in pourcent (Angles): "
          + str(np.sum(array_result)/len(array_result))
          + "%")

    return np.sum(array_result) / len(array_result), values
    pass

# =====================================================
# ======================= Area ========================
# =====================================================


def compare_mesh_list_area(meshs):
    """
        Compare_mesh_angle

        Compare all models by their areas with
        the first model (first trismesh of array).
        !!! Use display_plot() for the display of result !!!
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
        the first model in pourcent (first trismesh of array).
        !!! Use display_plot() for the display of result !!!
        (One display with histogram and one other with curve)

        :param meshs
        :type array [trimesh,trimesh,...]
    """

    mesh1 = meshs[0]
    array_result = []

    for i in range(1, len(meshs)):
        result = abs((meshs[i].area_faces/meshs[i].area)
                     - (mesh1.area_faces/mesh1.area))
        result_result = np.sum(result) * 100
        print(result_result)
        array_result.append(result_result)

    names = [(meshs[i].metadata['iters']) for i in range(1, len(meshs))]
    values = array_result

    # fig, ax = plt.subplots(1, 1)
    # plt.bar(names, values)
    # ax.set_title('Areas compare in pourcent')
    # ax.set_xlabel('Iterations')
    # ax.set_ylabel(' % difference areas')

    fig2, ax2 = plt.subplots(1, 1)
    ax2.plot(names, values, 'ro-')
    ax2.set_title('Areas compare in pourcent curve')
    ax2.set_xlabel('Iterations')
    ax2.set_ylabel('Areas compare in pourcent')

    print("Average of distortion in pourcent (Areas): "
          + str(np.sum(array_result)/len(array_result))
          + "%")

    return np.sum(array_result) / len(array_result), values
    pass


# ============================================================
# ======================= Edge length ========================
# ============================================================


def compare_mesh_list_edge_pourcent(meshs):
    """
        compare_mesh_list_area_curve_pourcent

        Compare all models by their edges with
        the first model in pourcent (first trismesh of array)
        !!! Use display_plot() for the display of result !!!
        (One display with histogram and one other with curve)

        :param meshs
        :type array [trimesh,trimesh,...]
    """
    mesh1 = meshs[0]
    array_result = []
    for i in range(1, len(meshs)):
        result = abs((meshs[i].edges_unique_length
                      / np.sum(meshs[i].edges_unique_length))
                     - (mesh1.edges_unique_length
                        / np.sum(mesh1.edges_unique_length)))
        result_result = np.sum(result) * 100
        print(result_result)
        array_result.append(result_result)

    names = [(meshs[i].metadata['iters'])
             for i in range(1, len(meshs))]  # len(meshs)

    values = array_result

    # fig, ax = plt.subplots(1, 1)
    # plt.bar(names, values)
    # ax.set_title('Edges compare in pourcent')
    # ax.set_xlabel('Iterations')
    # ax.set_ylabel(' % difference edge length')

    fig2, ax2 = plt.subplots(1, 1)
    ax2.plot(names, values, 'ro-')
    ax2.set_title('Edges compare in pourcent curve')
    ax2.set_xlabel('Iterations')
    ax2.set_ylabel('Edges compare in pourcent')

    print("Average of distortion in pourcent (Edges length): "
          + str(np.sum(array_result) / len(array_result))
          + "%")

    return np.sum(array_result) / len(array_result), values
    pass


# ========================================================================
# ======================= Superimpose the texture ========================
# ========================================================================


def superimpose_the_texture(mesh1, mesh2):
    """
        Superimpose_the_texture

        Take the texture of mesh2 and put on the mesh1

        :param mesh1
        :type trimesh

        :param mesh2
        :type trimesh

        :return new mesh1 with texture
    """

    mesh_copy = mesh1
    mesh_copy.visual.face_colors = mesh2.visual.face_colors

    return mesh_copy

    pass

# ==============================================================
# ======================= Display model/plot ===================
# ==============================================================


def display_model(mesh):
    """
        Display_model

        Display the model (by a window)

        :param mesh1
        :type trimesh
    """
    # splt.pyglet_plot(mesh1, np.array(result))

    splt.pyglet_plot(mesh)

    pass


def display_plot():
    """
        Display_plot

        Display of server (web) all the information in the plot
    """
    plt.show()

    pass
