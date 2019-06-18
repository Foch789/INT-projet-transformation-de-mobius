import numpy as np
from scipy.optimize import minimize
from scipy.optimize import dual_annealing

import trimesh

import matplotlib.pyplot as plt

import slam.plot as splt

import src.transformation_sphere as ts
import src.stereo_projection as sp

models = ['../model/foetus/foetus1.ply',
          '../model/foetus/foetus1_sphere.ply']

"""
================================================================================
======================= Load brain and sphere brain ============================
================================================================================
"""

model_base = trimesh.load(models[0])

model_sphere = trimesh.load(models[1])

model_sphere_color = model_sphere.copy()

# Display the sphere with color (Red = North / Blue = South)
splt.pyglet_plot(model_sphere_color, model_sphere_color.vertices[:, 2], caption="Sphere")


"""
=============================================================================
======================= Stereographic projection ============================
=============================================================================
"""

plan_sphere = sp.stereo_projection(model_sphere_color.vertices.copy())

# Load the new model Trimesh with the new vertices and color of the sphere.
plan_sphere_visu = trimesh.Trimesh(vertices=plan_sphere,
                                   faces=model_sphere_color.faces.copy(),
                                   vertex_colors=model_sphere_color.visual.vertex_colors.copy())

# Display the plan of the sphere
splt.pyglet_plot(plan_sphere_visu, caption="Plan sphere")


"""
========================================================================
======================= Plan with complex number =======================
========================================================================
"""

plan_complex = plan_sphere[:, 0] + (1.0j * plan_sphere[:, 1])


"""
===================================================================
======================= test random complex =======================
===================================================================
"""

# res = ts.random_complex(model_sphere_color, plan_complex, model_base)

res = ts.random_complex_with_minimize(model_sphere_color, plan_complex, model_base)

"""
==================================================================
======================= test angle complex =======================
==================================================================
"""

# res = mobius_angle_complex_a(model_sphere_color, plan_complex, model_base)

"""
================================================================================
======================= test minimize or dual_annealing  =======================
================================================================================
"""

# a = complex(1.0, 0.0)
# b = complex(0., 0.0)
# c = complex(0., 0.0)
# d = complex(1., 0.0)
#
# print(ts.complex_to_real([a, b, c, d]))
#
# array_area_result = []
# array_angle_result = []
#
# res = minimize(ts.func_for_minimize,
#                ts.complex_to_real([a, b, c, d]),
#                args=(plan_complex, model_sphere_color, model_base, array_angle_result, array_area_result),
#                method='Nelder-Mead',
#                options={'disp': True})
#
# # res = dual_annealing(ts.func_for_minimize,
# #                      bounds=npma.repmat([-100, 100], 8, 1),
# #                      args=(plan_complex, model_sphere_color, model_base))
# #
# res = ts.real_to_complex(res.x)
#
# array_name_minimize = []
#
# for i in range(0, len(array_area_result)):
#     array_name_minimize.append(i)
#
# fig, ax = plt.subplots(1, 1)
# plt.bar(array_name_minimize, array_angle_result)
# ax.set_title('Distorsion angle evolution minimize')
# ax.set_xlabel('Number of tests')
# ax.set_ylabel('% distorsion angle')
#
# fig, ax = plt.subplots(1, 1)
# plt.bar(array_name_minimize, array_area_result)
# ax.set_title('Distorsion area evolution minimize')
# ax.set_xlabel('Number of tests')
# ax.set_ylabel('% distorsion area')

"""
=========================================================================
======================= Compute the new plan ============================
=========================================================================
"""

plan_complex_transfo = ts.mobius_transformation(res[0], res[1], res[2], res[3], plan_complex)

real_array = plan_complex_transfo[:].real
imag_array = plan_complex_transfo[:].imag

result_plan_complex = []
for i in range(0, len(real_array)):
    result_plan_complex.append(np.array([real_array[i], imag_array[i], -1]))

result_plan_complex = np.array(result_plan_complex)

"""
=================================================================================================
======================= The new plan after the Möbius Transformation ============================
=================================================================================================
"""

plan_sphere_visu_transfo = trimesh.Trimesh(vertices=result_plan_complex,
                                           faces=model_sphere_color.faces.copy(),
                                           vertex_colors=model_sphere_color.visual.vertex_colors.copy())
splt.pyglet_plot(plan_sphere_visu_transfo)


"""
=================================================================================
======================= Inverse stereographic projection ========================
=================================================================================
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

plt.show()

result_angle = abs((model_transform_sphere.face_angles / np.sum(model_transform_sphere.face_angles))
                   - (model_base.face_angles / np.sum(model_base.face_angles)))
result_angle = np.sum(result_angle, axis=1)

result_area = abs((model_transform_sphere.area_faces / np.sum(model_transform_sphere.area_faces))
                  - (model_base.area_faces / np.sum(model_base.area_faces)))

splt.pyglet_plot(model_base, result_angle, plot_colormap=True, caption="Difference angle")
splt.pyglet_plot(model_base, result_area, plot_colormap=True, caption="Difference area")
splt.pyglet_plot(model_transform_sphere, result_area, caption="Difference area")
splt.pyglet_plot(model_transform_sphere, abs(model_transform_sphere.area_faces - model_sphere_color.area_faces), caption="Difference area between model no transfo and model transfo")