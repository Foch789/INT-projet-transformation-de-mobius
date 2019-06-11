from enum import Enum
from random import *
from scipy.optimize import minimize

import trimesh

import numpy as np
import matplotlib.pyplot as plt

import slam.io as sio
import slam.plot as splt

import src.model_treatment as mt
import src.transformation_sphere as ts
import src.stereo_projection as sp

models = ['../model/foetus/foetus1.ply',
          '../model/foetus/foetus1_sphere.ply']

"""
=========================================================
======================= Enum ============================
=========================================================
"""


class Operation(Enum):
    PLUS = 0
    MINUS = 1
    DIVISOR = 2
    ONE_DIVIDER_BY = 3
    TIMES = 4

result_all = []

"""
=========================================================
======================= Fonction ============================
=========================================================
"""


def real_to_complex(z):      # real vector of length 2n -> complex of length n
    return z[:len(z)//2] + 1j * z[len(z)//2:]


def complex_to_real(z):      # complex vector of length n -> real of length 2n
    return np.concatenate((np.real(z), np.imag(z)))


def test_param_mobius(param_model_sphere_color, plan_complex):

    result_all_angle = []
    result_all_area = []
    array_name = []
    array_result = []

    save_i_area = 0
    min_area = 1000000000.0

    save_i_angle = 0
    min_angle = 1000000000.0

    nbrAMin = -1000
    nbrAMax = 1000
    nbrAMin_IMAG = -1000
    nbrAMax_IMAG = 1000

    nbrBMin = -1000
    nbrBMax = 1000
    nbrBMin_IMAG = -1000
    nbrBMax_IMAG = 1000

    nbrCMin = -1000
    nbrCMax = 1000
    nbrCMin_IMAG = -1000
    nbrCMax_IMAG = 1000

    nbrDMin = -1000
    nbrDMax = 1000
    nbrDMin_IMAG = -1000
    nbrDMax_IMAG = 1000

    for i in range(1, 100):

        a = complex(uniform(nbrAMin, nbrAMax), uniform(nbrAMin_IMAG, nbrAMax_IMAG))
        b = complex(uniform(nbrBMin, nbrBMax), uniform(nbrBMin_IMAG, nbrBMax_IMAG))
        c = complex(uniform(nbrCMin, nbrCMax), uniform(nbrCMin_IMAG, nbrCMax_IMAG))
        d = complex(uniform(nbrDMin, nbrDMax), uniform(nbrDMin_IMAG, nbrDMax_IMAG))

        array_result.append("" + str(a) + " | " + str(b) + " | " + str(c) + " | " + str(d) + "")

        array_name.append(i)

        plan_complex_transfo = ts.mobius_transformation(a, b, c, d, plan_complex)

        real_array = plan_complex_transfo[:].real
        imag_array = plan_complex_transfo[:].imag

        result_plan_complex = []
        for p in range(0, len(real_array)):
            result_plan_complex.append(np.array([real_array[p], imag_array[p], -1]))

        result_plan_complex = np.array(result_plan_complex)

        new_vertices_sphere = sp.inverse_stereo_projection(result_plan_complex)
        model_transform_sphere = trimesh.Trimesh(vertices=new_vertices_sphere,
                                   faces=param_model_sphere_color.faces,
                                   vertex_colors=param_model_sphere_color.visual.vertex_colors)


        result_angle = abs((model_transform_sphere.face_angles / np.sum(model_transform_sphere.face_angles))
                           - (param_model_sphere_color.face_angles / np.sum(param_model_sphere_color.face_angles)))
        result_angle_pourcent = np.sum(result_angle) * 100

        result_all_angle.append(result_angle_pourcent)

        result_area = abs((model_transform_sphere.area_faces / np.sum(model_transform_sphere.area_faces))
                          - (param_model_sphere_color.area_faces / np.sum(param_model_sphere_color.area_faces)))

        result_area_pourcent = np.sum(result_area) * 100

        result_all_area.append(result_area_pourcent)

        if min_angle > result_angle_pourcent:
            min_angle = result_angle_pourcent
            save_i_angle = i

        if min_area > result_area_pourcent:
            save_i_area = i
            min_area = result_area_pourcent

            print(save_i_area)
            #splt.pyglet_plot(model_transform_sphere)

            if a.real >= 0:
                nbrAMax = a.real
            else:
                nbrAMin = a.real
            if a.imag >= 0:
                nbrAMax_IMAG = a.imag
            else:
                nbrAMin_IMAG = a.imag

            if b.real >= 0:
                nbrBMax = b.real
            else:
                nbrBMin = b.real
            if b.imag >= 0:
                nbrBMax_IMAG = b.imag
            else:
                nbrBMin_IMAG = b.imag

            if c.real >= 0:
                nbrCMax = c.real
            else:
                nbrCMin = c.real
            if c.imag >= 0:
                nbrCMax_IMAG = c.imag
            else:
                nbrCMin_IMAG = c.imag

            if d.real >= 0:
                nbrDMax = d.real
            else:
                nbrDMin = d.real
            if d.imag >= 0:
                nbrDMax_IMAG = d.imag
            else:
                nbrDMin_IMAG = d.imag


    fig, ax = plt.subplots(1, 1)
    plt.bar(array_name, result_all_angle)
    ax.set_title('Distorsion angle ')
    ax.set_xlabel('Number of tests')
    ax.set_ylabel('% distorsion angle')

    fig, ax = plt.subplots(1, 1)
    plt.bar(array_name, result_all_area)
    ax.set_title('Distorsion area ')
    ax.set_xlabel('Number of tests')
    ax.set_ylabel('% distorsion area')

    print("Regarder le " + str(save_i_area) + " avec " + str(result_all_area[save_i_area-1]) + "% de distorsion d'aires")
    print("Regarder le " + str(save_i_angle) + " avec " + str(result_all_angle[save_i_angle-1]) + "% de distorsion d'angles")

    return array_result


result_all_angle_pourcent = []
result_all_area_pourcent = []


def fonc(x, plan_complex, param_model_sphere_color, model_base):

    a = real_to_complex(x)[0]
    b = real_to_complex(x)[1]
    c = real_to_complex(x)[2]
    d = real_to_complex(x)[3]

    plan_complex_transfo = ts.mobius_transformation(a, b, c, d, plan_complex)

    real_array = plan_complex_transfo[:].real
    imag_array = plan_complex_transfo[:].imag

    result_plan_complex = []
    for p in range(0, len(real_array)):
        result_plan_complex.append(np.array([real_array[p], imag_array[p], -1]))

    result_plan_complex = np.array(result_plan_complex)

    new_vertices_sphere = sp.inverse_stereo_projection(result_plan_complex)
    model_transform_sphere = trimesh.Trimesh(vertices=new_vertices_sphere,
                                             faces=param_model_sphere_color.faces,
                                             vertex_colors=param_model_sphere_color.visual.vertex_colors)

    result_angle = abs((model_transform_sphere.face_angles / np.sum(model_transform_sphere.face_angles))
                       - (param_model_sphere_color.face_angles / np.sum(param_model_sphere_color.face_angles)))

    result_angle_pourcent = np.sum(result_angle) * 100

    result_all_angle_pourcent.append(result_angle_pourcent)

    result_area = abs((model_transform_sphere.area_faces / np.sum(model_transform_sphere.area_faces))
                      - (model_base.area_faces / np.sum(model_base.area_faces)))

    result_area_pourcent = np.sum(result_area) * 100

    result_all_area_pourcent.append(result_area_pourcent)

    return result_area_pourcent


"""
=========================================================
======================= Base ============================
=========================================================
"""

model_base = trimesh.load(models[0])

model_sphere = trimesh.load(models[1])

model_sphere_color = ts.vertex_color_sphere(model_sphere)


"""
=========================================================
======================= Plan ============================
=========================================================
"""

plan_sphere = sp.stereo_projection(model_sphere_color.vertices.copy())
plan_sphere_visu = trimesh.Trimesh(vertices=plan_sphere,
                                   faces=model_sphere_color.faces.copy(),
                                   vertex_colors=model_sphere_color.visual.vertex_colors.copy())
splt.pyglet_plot(plan_sphere_visu)


"""
=========================================================
======================= Complex =======================
=========================================================
"""

plan_complex = plan_sphere[:, 0] + (1.0j * plan_sphere[:, 1])

a = complex(1.0, 0.0)
b = complex(10.0, 1.0)
c = complex(10.0, 1.0)
d = complex(10.0, 1.0)

res = minimize(fonc,
               complex_to_real([a, b, c, d]),
               args=(plan_complex, model_sphere_color, model_base),
               method='BFGS')

res = real_to_complex(res.x)

print(res)

# array_machin = test_param_mobius(model_sphere_color, plan_complex)

plan_complex_transfo = ts.mobius_transformation(res[0], res[1], res[2], res[3], plan_complex)

real_array = plan_complex_transfo[:].real
imag_array = plan_complex_transfo[:].imag

result_plan_complex = []
for i in range(0, len(real_array)):
    result_plan_complex.append(np.array([real_array[i], imag_array[i], -1]))

result_plan_complex = np.array(result_plan_complex)

plan_sphere_visu_transfo = trimesh.Trimesh(vertices=result_plan_complex,
                                           faces=model_sphere_color.faces.copy(),
                                           vertex_colors=model_sphere_color.visual.vertex_colors.copy())
splt.pyglet_plot(plan_sphere_visu_transfo)



"""
=========================================================
======================= Inverse ========================
=========================================================
"""

new_vertices_sphere = sp.inverse_stereo_projection(result_plan_complex)
model_transform_sphere = trimesh.Trimesh(vertices=new_vertices_sphere,
                                         faces=model_sphere_color.faces,
                                         vertex_colors=model_sphere_color.visual.vertex_colors)
splt.pyglet_plot(model_transform_sphere)


"""
=========================================================
======================= Histogram =======================
=========================================================
"""
tab = []

for i in range(0, len(result_all_angle_pourcent)):
    tab.append(i)


# fig, ax = plt.subplots(1, 1)
# plt.bar(tab, result_all_angle_pourcent)
# ax.set_title('Distorsion angle ')
# ax.set_xlabel('Number of tests')
# ax.set_ylabel('% distorsion angle')
#
# fig, ax = plt.subplots(1, 1)
# plt.bar(tab, result_all_area_pourcent)
# ax.set_title('Distorsion area ')
# ax.set_xlabel('Number of tests')
# ax.set_ylabel('% distorsion area')


result_all = []

result_angle = abs((model_transform_sphere.face_angles/np.sum(model_transform_sphere.face_angles))
                   - (model_base.face_angles/np.sum(model_base.face_angles)))
result_angle_pourcent = np.sum(result_angle) * 100
print(result_angle_pourcent)

result_all.append(result_angle_pourcent)

result_area = abs((model_transform_sphere.area_faces/np.sum(model_transform_sphere.area_faces))
                  - (model_base.area_faces/np.sum(model_base.area_faces)))

result_area_pourcent = np.sum(result_area) * 100
print(result_area_pourcent)

result_all.append(result_area_pourcent)

result_all.append(result_angle_pourcent + result_area_pourcent)

fig, ax = plt.subplots(1, 1)
plt.bar(["Angle", "Area", "Global"], result_all)
ax.set_title('Distorsion')
ax.set_xlabel('Transform sphere')
ax.set_ylabel('% distorsion')

# plt.show()


splt.pyglet_plot(model_base,result_area,caption="Difference area")
splt.pyglet_plot(model_transform_sphere, result_area, caption="Difference area")
splt.pyglet_plot(model_transform_sphere, abs(model_transform_sphere.area_faces - model_sphere_color.area_faces), caption="Difference area between model no transfo and model transfo")



# nn = 0
# taille = len(array_machin)
# while nn != -1:
#     print("Veuillez entrer un nombre entre 0 " + str(taille) + " :")
#     nn = int(input()) or -1
#     if nn != -1:
#         print(array_machin[nn])
