from src.model_treatment import *
import slam.texture as texture

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

array_distorsion_angles = dist.angle_difference(meshs[0], meshs[9])
array_distorsion_areas = dist.area_difference(meshs[0], meshs[9])
array_distorsion_edges_length = []

for i in range(0, len(meshs[0].faces_unique_edges)):
    res = 0
    for p in meshs[0].faces_unique_edges[i]:
        res += np.abs(meshs[0].edges_unique_length[p] - meshs[9].edges_unique_length[p])
    res = res/3
    array_distorsion_edges_length.insert(i, res)

darray_angles = np.array(array_distorsion_angles)
tex_angles = texture.TextureND(darray=darray_angles)
print(len(tex_angles.darray))

darray_areas = np.array(array_distorsion_areas)
tex_areas = texture.TextureND(darray=darray_areas)
print(len(tex_areas.darray))

darray_edges_length = np.array(array_distorsion_edges_length)
tex_edges_length = texture.TextureND(darray=darray_edges_length)
print(len(tex_edges_length.darray))

tex_sum = np.sum(np.abs(tex_angles.darray), 1 ) # seulement pour les angles

print("Le min de distorsion d'angle : " + str(tex_sum.min()) + " et le max : " + str(tex_sum.max()))

splt.pyglet_plot(meshs[0], tex_sum, map_min=tex_sum.min(), map_max=tex_sum.max(), plot_colormap=False)

print("Le min de distorsion d'aires : " + str(tex_areas.min()) + " et le max : " + str(tex_areas.max()))

splt.pyglet_plot(meshs[0], tex_areas.darray, map_min=tex_areas.min(), map_max=tex_areas.max(), plot_colormap=False)

print("Le min de distorsion de longueur d'arête : " + str(tex_edges_length.min()) + " et le max : " + str(tex_edges_length.max()))

splt.pyglet_plot(meshs[0], tex_edges_length.darray, map_min=tex_edges_length.min(), map_max=tex_edges_length.max(), plot_colormap=False)
#splt.pyglet_plot(meshs[9], tex_edges_length.darray, map_min=tex_edges_length.min(), map_max=tex_edges_length.max())