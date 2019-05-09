import numpy as np
import trimesh
import trimesh.visual.color as col
import matplotlib.pyplot as plt
import multiprocessing as mp

import slam.distortion as dist
import slam.plot as splt

# =====================================================
# ======================= Angle =======================
# =====================================================


def compare_mesh_angle(mesh1,mesh2):
    """
        Compare_mesh_angle

        Compare the angles of 2 trimesh and add information (difference between 2 models) in plot

        :param mesh1
        :type trimesh

        :param mesh2
        :type trimesh
    """

    return dist.angle_difference(mesh1, mesh2)

    pass


def compare_mesh_list_angle(meshs):
    """
        Compare_mesh_list_angle

        Compare all models by their angles with the first model (first trismesh of array)

        :param meshs
        :type array [trimesh,trimesh,...]
    """

    mesh1 = meshs[0]
    for i in range(1, len(meshs)):
        angle_diff = compare_mesh_angle(mesh1, meshs[i])
        f, ax = plt.subplots(1, 1)
        ax.set_title('angles compare ' + mesh1.metadata['name'] + " to " + meshs[i].metadata['name'])
        ax.hist(angle_diff.flatten(), 100)
        ax.grid(True)

    pass


def compare_mesh_list_angle_pourcent(meshs):
    """
        compare_mesh_list_area_curve_pourcent

        Compare all models by their areas with the first model in pourcent (first trismesh of array)

        :param meshs
        :type array [trimesh,trimesh,...]
    """

    mesh1 = meshs[0]
    array_result = []

    for i in range(1, len(meshs)):
        result = list()
        result.append(compare_mesh_angle(mesh1, meshs[i]))
        print(np.sum(np.abs(result)/np.sum(mesh1.face_angles))*100)
        array_result.append(np.sum(np.abs(result)/np.sum(mesh1.face_angles))*100)

    names = [(meshs[i].metadata['iters']) for i in range(1, len(meshs))]
    values = array_result

    fig, ax = plt.subplots(1, 1)
    plt.bar(names, values)
    ax.set_title('Angles compare in pourcent')
    ax.set_xlabel('Iterations')
    ax.set_ylabel(' % difference angles')
    pass

# =====================================================
# ======================= Area ========================
# =====================================================


def compare_mesh_area(mesh1, mesh2):
    """
        Compare_mesh_area

        Compare the areas of 2 trimesh and add information (difference between 2 models) in plot

        :param mesh1
        :type trimesh

        :param mesh2
        :type trimesh
    """

    return dist.area_difference(mesh1, mesh2)

    pass


def compare_mesh_list_area(meshs):
    """
        Compare_mesh_angle

        Compare all models by their areas with the first model (first trismesh of array)

        :param meshs
        :type array [trimesh,trimesh,...]
    """

    mesh1 = meshs[0]
    for i in range(1, len(meshs)):
        area_diff = compare_mesh_area(mesh1, meshs[i])
        f, ax = plt.subplots(1, 1)
        ax.set_title('areas compare ' + mesh1.metadata['name'] + " to " + meshs[i].metadata['name'])
        ax.hist(area_diff.flatten(), 100)
        ax.grid(True)

    pass


def compare_mesh_list_area_curve(meshs):
    """
        compare_mesh_list_area_curve

        Compare all models by their areas with the first model (first trismesh of array) and draw a curve

        :param meshs
        :type array [trimesh,trimesh,...]
    """

    mesh1 = meshs[0]
    array_area_diff_sum = []
    array_temp = 0
    max_sum_area = 0
    for i in range(1, len(meshs)):
        area_diff = compare_mesh_area(mesh1, meshs[i])

        for p in range(0, len(area_diff)):
            array_temp += area_diff[p]

        if max_sum_area < array_temp:
            max_sum_area = array_temp
        print(array_temp)
        array_area_diff_sum.append(array_temp)

    fig, ax = plt.subplots(1, 1)
    ax.plot([(meshs[i].metadata['iters']) for i in range(1, len(meshs))], array_area_diff_sum, 'ro-')
    ax.set_title('areas compare')
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Sum areas')
    ax.axis([0, meshs[len(meshs) - 1].metadata['iters'] + (meshs[len(meshs) - 1].metadata['iters'] / 4), 0,
             max_sum_area + (max_sum_area / 4)])
    plt.show()

    pass


def compare_mesh_list_area_pourcent(meshs):
    """
        compare_mesh_list_area_curve_pourcent

        Compare all models by their areas with the first model in pourcent (first trismesh of array)

        :param meshs
        :type array [trimesh,trimesh,...]
    """

    mesh1 = meshs[0]
    array_result = []
    for i in range(1, len(meshs)):
        result = list()
        for p in range(0, len(meshs[i].area_faces)):
            result.append((meshs[i].area_faces[p]/meshs[i].area - mesh1.area_faces[p]/mesh1.area))
        result_result = np.sum(np.abs(result)) * 100
        print(result_result)
        array_result.append(result_result)

    #splt.pyglet_plot(mesh1, np.array(result))

    names = [(meshs[i].metadata['iters']) for i in range(1, len(meshs))]
    values = array_result

    fig, ax = plt.subplots(1, 1)
    plt.bar(names, values)
    ax.set_title('Areas compare in pourcent')
    ax.set_xlabel('Iterations')
    ax.set_ylabel(' % difference areas')
    pass


# ============================================================
# ======================= Edge length ========================
# ============================================================


def compare_mesh_list_edge_pourcent(meshs):
    """
        compare_mesh_list_area_curve_pourcent

        Compare all models by their areas with the first model in pourcent (first trismesh of array)

        :param meshs
        :type array [trimesh,trimesh,...]
    """

    mesh1 = meshs[0]
    array_result = []
    for i in range(1, len(meshs)):
        result = list()
        for p in range(0, len(meshs[i].edges_unique_length)):
            result.append(abs((meshs[i].edges_unique_length[p] / np.sum(meshs[i].edges_unique_length) -
                               mesh1.edges_unique_length[p] / np.sum(mesh1.edges_unique_length))))
        result_result = np.sum(np.abs(result)) * 100
        print(result_result)
        array_result.append(result_result)

    names = [(meshs[i].metadata['iters']) for i in range(1, len(meshs))]
    values = array_result

    fig, ax = plt.subplots(1, 1)
    plt.bar(names, values)
    ax.set_title('Edges compare in pourcent')
    ax.set_xlabel('Iterations')
    ax.set_ylabel(' % difference edge length')
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
    """

    mesh1.visual.face_colors = mesh2.visual.face_colors

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
    splt.pyglet_plot(mesh)

    pass


def display_plot():

    """
        Display_plot

        Display of server (web) all the information in the plot
    """
    plt.show()

    pass
