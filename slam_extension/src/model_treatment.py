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

    angle_diff = dist.angle_difference(mesh1, mesh2)

    f, ax = plt.subplots(1, 1)
    ax.set_title('angles compare ' + mesh1.metadata['name'] + " to " + mesh2.metadata['name'])
    ax.hist(angle_diff.flatten(), 100)
    ax.grid(True)

    pass


def compare_mesh_list_angle(meshs):
    """
        Compare_mesh_angle

        :param mesh1
        :type array [file_name,trimesh,...]
    """

    mesh1 = meshs[0]
    for i in range(1, len(meshs)):
        compare_mesh_angle(mesh1, meshs[i])

    pass

# =====================================================
# ======================= Area ========================
# =====================================================


def compare_mesh_area(mesh1, mesh2):
    """
        Compare_mesh_angle

        :param mesh1
        :type array [file_name,trimesh,...]

        :param mesh2
        :type array [file_name,trimesh,...]
    """

    area_diff = dist.area_difference(mesh1, mesh2)

    f, ax = plt.subplots(1, 1)
    ax.set_title('areas compare ' + mesh1.metadata['name'] + " to " + mesh2.metadata['name'])
    ax.hist(area_diff.flatten(), 100)
    ax.grid(True)

    # splt.pyglet_plot(mesh1)
    # splt.pyglet_plot(mesh2)

    pass


def compare_mesh_list_area(meshs):
    """
        Compare_mesh_angle

        :param mesh
        :type array [file_name,trimesh]
    """

    mesh1 = meshs[0]
    for i in range(1, len(meshs)):
        compare_mesh_area(mesh1, meshs[i])

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

