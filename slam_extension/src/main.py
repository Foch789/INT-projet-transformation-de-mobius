import sys
import numpy as np
import trimesh
import trimesh.exchange.ply as plyl
import matplotlib.pyplot as plt

import slam.io as sio
import slam.plot as splt
import slam.distortion as dist
import slam.texture as texture

from src.model_treatment import *

# import multiprocessing as mp
# pool = mp.Pool(mp.cpu_count())

"""
/distorsion longueur d'arrête + plot
Vérification du même nombre de point  
Texture
"""

# Path of models
args = ['../model/brain.ply',#0
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

# '../model/brain.cmcf.ply',  # 11
# '../model/brain_1_.cmcf.ply'  # 12

file_foetus = ['../model/foetus/foetus1.ply',#0
               '../model/foetus/foetus2.ply',#1
               '../model/foetus/foetus_sphere1.cmcf.ply',#2
               '../model/foetus/foetus_sphere2.cmcf.ply',#3
               '../model/foetus/foetus_register.ply'#4
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


def main(argv):
    """
    if len(argv) >= 2:
    else:
        print("No ... you have to put model in var 'args'")
    """

    if len(args) >= 2:
        meshs = []
        for i in range(0, len(args)):
            print(args[i])
            mesh = trimesh.load(args[i])
            mesh.metadata = {'name': name_fil(args[i]), 'iters': iters[i]}
            # mesh.export(name_fil(args[i])[-4]+'ascii.ply', encoding='ascii')
            # sio.write_mesh(mesh, name_fil(args[i])[-4]+'gii')
            meshs.append(mesh)

        # compare_mesh_list_angle(meshs)
        # average_angle, values_angles = compare_mesh_list_angle_pourcent(meshs)

        # compare_mesh_list_area(meshs)
        # average_area, values_areas = compare_mesh_list_area_pourcent(meshs)

        # compare_mesh_list_edge(meshs)
        # average_edge_length, values_edges = compare_mesh_list_edge_pourcent(meshs)

        """
        =======================================================================================
        ================================ Distortion difference ================================
        =======================================================================================
        """

        # names = [(meshs[i].metadata['iters']) for i in range(1, len(meshs))]
        # values = []
        # for i in range(0, len(meshs)-1):
        #     print(values_angles[i] + values_areas[i] + values_edges[i])
        #     values.append(values_angles[i] + values_areas[i] + values_edges[i])
        #
        # print("Average of distortion in pourcent : " + str(average_angle + average_area + average_edge_length / 3) + "%")

        # fig, ax = plt.subplots(1, 1)
        # plt.bar(names, values)
        # ax.set_title('Distortion compare in pourcent')
        # ax.set_xlabel('Iterations')
        # ax.set_ylabel(' % difference distortion')

        # fig2, ax2 = plt.subplots(1, 1)
        # ax2.plot(names, values, 'ro-')
        # ax2.set_title('Distortion compare in pourcent curve')
        # ax2.set_xlabel('Iterations')
        # ax2.set_ylabel('Distortion compare in pourcent')

        """
        =========================================================================
        ================================ Display ================================
        =========================================================================
        """

        # display_plot()

        #f1 = trimesh.load(file_foetus[0])
        #f2 = trimesh.load(file_foetus[1])
        #f3 = trimesh.load(file_foetus[4])
        #display_model(f1)
        #display_model(f2)
        #display_model(f3)

        # display_model(meshs[0])
        # display_model(meshs[9])
        # superimpose_the_texture(meshs[0], meshs[9])
        # display_model(meshs[0])

        """
        =============================================================================
        ================================ Other tests ================================
        =============================================================================
        """
        # fp = open('../model/brain.ply')
        # plyl.parse_header(fp)

        """
        ================================================================================================
        ================================ Transform gii file to ply file ================================
        ================================================================================================
        """

        # mesh_export = sio.load_mesh("../model/foetus.gii")
        # mesh_export.export("foetus.ply")

        # mesh_export = sio.load_mesh("../model/foetus1.gii")
        # mesh_export.export("foetus1.ply")
        #
        # mesh_export = sio.load_mesh("../model/foetus2.gii")
        # mesh_export.export("foetus2.ply")

        """
        ==============================================================================================
        ================================ Texture sphere on base model ================================
        ==============================================================================================
        """

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

        # splt.pyglet_plot(meshs[0], tex_sum, map_min=tex_sum.min(), map_max=tex_sum.max(), plot_colormap=True)

        print("Le min de distorsion d'aires : " + str(tex_areas.min()) + " et le max : " + str(tex_areas.max()))

        # splt.pyglet_plot(meshs[0], tex_areas.darray, map_min=tex_areas.min(), map_max=tex_areas.max(), plot_colormap=True)

        print("Le min de distorsion de longueur d'arête : " + str(tex_edges_length.min()) + " et le max : " + str(tex_edges_length.max()))

        splt.pyglet_plot(meshs[0], tex_edges_length.darray, map_min=tex_edges_length.min(), map_max=tex_edges_length.max(), plot_colormap=True)
        #splt.pyglet_plot(meshs[9], tex_edges_length.darray, map_min=tex_edges_length.min(), map_max=tex_edges_length.max())


    else:
        print("No ... you have to put path of model in var 'args' (min 2 models)")

    pass


""" CORRECT THIS FUNC """


def name_fil(path_file):
    path_file = str(path_file)
    name = ""
    for i in range(path_file.find("brain"), len(path_file)):
        name += (path_file[i])

    return name


if __name__ == "__main__":
    main(sys.argv[1:])