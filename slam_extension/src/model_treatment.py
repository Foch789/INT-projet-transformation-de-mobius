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

        :param mesh1
        :type trimesh

        :param mesh2
        :type trimesh
    """

    angle_diff = dist.angle_difference(mesh1[1], mesh2[1])

    f, ax = plt.subplots(1, 1)
    ax.set_title('angles compare ' + mesh1[0] + " to " + mesh2[0])
    ax.hist(angle_diff.flatten(), 100)
    ax.grid(True)

    # splt.pyglet_plot(mesh1)
    # splt.pyglet_plot(mesh2)

    pass


def mesh_angle(meshs):

    """
        Compare_mesh_angle

        :param mesh1
        :type array [file_name,trimesh,...]
    """

    mesh1 = [meshs[0], meshs[1]]
    i = 2
    while i != len(meshs):
        mesh2 = []
        mesh2.append(meshs[i])
        i += 1
        mesh2.append(meshs[i])
        i += 1
        compare_mesh_angle(mesh1, mesh2)

    pass

# =====================================================
# ======================= Area ========================
# =====================================================


def area_diffference(mesh1, mesh2):

    """
        Compare_mesh_angle

        :param mesh1
        :type trimesh

        :param mesh2
        :type trimesh

        :return
    """

    return mesh1.area_faces - mesh2.area_faces


def compare_mesh_area(mesh1, mesh2):

    """
        Compare_mesh_angle

        :param mesh1
        :type array [file_name,trimesh,...]

        :param mesh2
        :type array [file_name,trimesh,...]
    """

    area_diff = area_diffference(mesh1[1], mesh2[1])

    f, ax = plt.subplots(1, 1)
    ax.set_title('areas compare ' + mesh1[0] + " to " + mesh2[0])
    ax.hist(area_diff.flatten(), 100)
    ax.grid(True)

    # splt.pyglet_plot(mesh1)
    # splt.pyglet_plot(mesh2)

    pass


def mesh_area(meshs):

    """
        Compare_mesh_angle

        :param mesh
        :type array [file_name,trimesh]
    """

    mesh1 = [meshs[0], meshs[1]]
    i = 2

    while i != len(meshs):
        mesh2 = []
        mesh2.append(meshs[i])
        i += 1
        mesh2.append(meshs[i])
        i += 1
        compare_mesh_area(mesh1, mesh2)

    pass


# ========================================================================
# ======================= Superimpose the texture ========================
# ========================================================================


def superimpose_the_texture(mesh1, mesh2):

    """
        Compare_mesh_angle

        :param mesh1
        :type trimesh

        :param mesh2
        :type trimesh
    """

    mesh1.visual.face_colors = mesh2.visual.face_colors

    pass

# ==============================================================
# ======================= Display model/plot ========================
# ==============================================================





def display_model(mesh):

    """
        Compare_mesh_angle

        :param mesh1
        :type trimesh
    """

    # pool = mp.Pool(mp.cpu_count())

    # pool.starmap(disp, [(meshs[i]) for i in range(0, len(meshs))])

    # pool.close()

    splt.pyglet_plot(mesh)

    # mesh.show()

    pass


def display_plot():

    """
        Compare_mesh_angle

        :param mesh1
        :type trimesh

        :param mesh2
        :type trimesh
    """
    plt.show()

    pass

