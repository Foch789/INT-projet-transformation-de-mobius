import trimesh
import numpy as np
import slam.plot as splt


def name_fil(path_file):
    """
        name_fil

        Take juste the name of the file

        :param path_file: Path of the file

        :return the name of the file
    """
    path_file = str(path_file)
    name = ""
    for it in range(path_file.find("brain"), len(path_file)):
        name += (path_file[it])

    return name


"""
=============================================================================
========================== Transform in var Trimesh =========================
=============================================================================
"""


model = ['../model/brain/brain.ply',  # 0
         '../model/brain/brain_sphere_1_iters.ply',  # 1
         '../model/brain/brain_sphere_2_iters.ply',  # 2
         '../model/brain/brain_sphere_4_iters.ply',  # 3
         '../model/brain/brain_sphere_8_iters.ply',  # 4
         '../model/brain/brain_sphere_16_iters.ply',  # 5
         '../model/brain/brain_sphere_32_iters.ply',  # 6
         '../model/brain/brain_sphere_50_iters.ply',  # 7
         '../model/brain/brain_sphere_75_iters.ply',  # 8
         '../model/brain/brain_sphere_100_iters.ply',  # 9
         '../model/brain/brain_sphere_200_iters.ply'  # 10
         ]

meshs = []
for i in range(0, len(model)):
    print(model[i])
    mesh = trimesh.load(model[i])
    mesh.metadata = {'name': name_fil(model[i])}
    meshs.append(mesh)

"""
=============================================================================
========================== Compute de distortion =========================
=============================================================================
"""


array_distorsion_angles = abs((meshs[0].face_angles/np.sum(meshs[0].face_angles))
                              - (meshs[9].face_angles/np.sum(meshs[9].face_angles)))

array_distorsion_angles = np.sum(array_distorsion_angles, axis=1)

array_distorsion_areas = abs((meshs[0].area_faces/np.sum(meshs[0].area_faces))
                             - (meshs[9].area_faces/np.sum(meshs[9].area_faces)))


"""
===============================================================================================
========================== Display on the brain to see the distortion =========================
===============================================================================================
"""

splt.pyglet_plot(meshs[0], array_distorsion_angles, caption="Difference angle")

splt.pyglet_plot(meshs[0], array_distorsion_areas, caption="Difference area")
