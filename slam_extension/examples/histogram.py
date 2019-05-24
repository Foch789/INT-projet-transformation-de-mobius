import trimesh
import matplotlib.pyplot as plt

from src.model_treatment import *



def name_fil(path_file):
    path_file = str(path_file)
    name = ""
    for i in range(path_file.find("brain"), len(path_file)):
        name += (path_file[i])

    return name


model = ['../model/brain.ply',#0
        '../model/brain_sphere_1_iters.ply',#1
        '../model/brain_sphere_2_iters.ply',#2
        '../model/brain_sphere_4_iters.ply',#3
        '../model/brain_sphere_8_iters.ply',#4
        '../model/brain_sphere_16_iters.ply',#5
        '../model/brain_sphere_32_iters.ply',#6
        '../model/brain_sphere_50_iters.ply',#7
        '../model/brain_sphere_75_iters.ply',#8
        '../model/brain_sphere_100_iters.ply',#9
        '../model/brain_sphere_200_iters.ply'#10
        ]

iters = [0,
         1,
         2,
         4,
         8,
         16,
         32,
         50,
         75,
         100,
         200
         ]

if len(model) >= 2:
    meshs = []
    for i in range(0, len(model)):
        print(model[i])
        mesh = trimesh.load(model[i])
        mesh.metadata = {'name': name_fil(model[i]), 'iters': iters[i]}
        meshs.append(mesh)


average_angle, values_angles = compare_mesh_list_angle_pourcent(meshs)

average_area, values_areas = compare_mesh_list_area_pourcent(meshs)

average_edge_length, values_edges = compare_mesh_list_edge_pourcent(meshs)



"""
=======================================================================================
================================ Distortion difference ================================
=======================================================================================
"""

names = [(meshs[i].metadata['iters']) for i in range(1, len(meshs))]
values = []
for i in range(0, len(meshs)-1):
    print(values_angles[i] + values_areas[i] + values_edges[i])
    values.append(values_angles[i] + values_areas[i] + values_edges[i])

print("Average of distortion in pourcent : " + str(average_angle + average_area + average_edge_length / 3) + "%")

# fig, ax = plt.subplots(1, 1)
# plt.bar(names, values)
# ax.set_title('Distortion compare in pourcent')
# ax.set_xlabel('Iterations')
# ax.set_ylabel(' % difference distortion')

fig2, ax2 = plt.subplots(1, 1)
ax2.plot(names, values, 'ro-')
ax2.set_title('Distortion compare in pourcent curve')
ax2.set_xlabel('Iterations')
ax2.set_ylabel('Distortion compare in pourcent')

# Display
display_plot()
