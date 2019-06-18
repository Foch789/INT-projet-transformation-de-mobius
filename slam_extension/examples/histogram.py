import trimesh
import matplotlib.pyplot as plt

import src.compare_model as mt


def name_fil(path_file):
    """
        name_fil

        Take juste the name of the file

        :param path_file
        :type String

        :return the name of the file
        :type String
    """
    path_file = str(path_file)
    name = ""
    for p in range(path_file.find("brain"), len(path_file)):
        name += (path_file[p])

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
    mesh = trimesh.load(model[i])
    mesh.metadata = {'name': name_fil(model[i])}
    meshs.append(mesh)


"""
==============================================================================================
========================== Use functions by the file "compare_model" =========================
==============================================================================================
"""


average_angle, values_angles = mt.compare_mesh_list_angle_pourcent(meshs)

average_area, values_areas = mt.compare_mesh_list_area_pourcent(meshs)

average_edge_length, values_edges = mt.compare_mesh_list_edge_pourcent(meshs)


"""
======================================================================================
========================== Distortion difference in general ==========================
======================================================================================
"""

names = [i for i in range(1, len(meshs))]
values = []
for i in range(0, len(meshs)-1):
    print(values_angles[i] + values_areas[i] + values_edges[i])
    values.append(values_angles[i] + values_areas[i] + values_edges[i])

print("Average of distortion general in pourcent : " +
      str(average_angle + average_area + average_edge_length / 3) + "%")


fig2, ax2 = plt.subplots(1, 1)
ax2.plot(names, values, 'ro-')
ax2.set_title('Distortion general compare in pourcent curve')
ax2.set_xlabel('Model to compare')
ax2.set_ylabel('Distortion compare in pourcent')

plt.show()
