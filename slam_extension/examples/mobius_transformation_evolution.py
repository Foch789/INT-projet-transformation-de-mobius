import numpy as np
from scipy.optimize import minimize
from scipy.optimize import dual_annealing

import trimesh

import matplotlib.pyplot as plt

import slam.plot as splt

import src.transformation_sphere as ts
import src.compare_model as cp
import src.stereo_projection as sp

models = ['../model/foetus/foetus1.ply',
          '../model/foetus/foetus1_sphere.ply',
          '../model/brain/brain.ply',
          '../model/brain/brain_sphere_100_iters.ply']

"""
================================================================================
======================= Load brain and sphere brain ============================
================================================================================
"""

model_base = trimesh.load(models[0])  # Foetus
model_sphere = trimesh.load(models[1])  # Foetus sphere
meshs = [model_base, model_sphere]

splt.pyglet_plot(model_base, caption="Foetus")


cp.compare_mesh_list_angle_pourcent(meshs)
cp.compare_mesh_list_area_pourcent(meshs)

model_sphere_color = model_sphere.copy()

# Display the sphere with color (Red = North / Blue = South)
splt.pyglet_plot(model_sphere_color, model_sphere_color.vertices[:, 2], caption="Sphere")

plt.show()

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

res = ts.random_complex_median(model_sphere_color, plan_complex, model_base, min_random=-100,
                        max_random=100, nbr_iteration=1000)

res = ts.random_complex_average(model_sphere_color, plan_complex, model_base, min_random=-100,
                        max_random=100, nbr_iteration=1000)

res = ts.random_complex_abs_value_pourcent(model_sphere_color, plan_complex, model_base, min_random=-100,
                        max_random=100, nbr_iteration=1000)

# res = ts.random_complex_with_minimize(model_sphere_color, plan_complex, model_base)

"""
==================================================================
======================= test angle complex =======================
==================================================================
"""

# res = ts.mobius_angle_complex_a(model_sphere_color, plan_complex, model_base)

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
# res = ts.algo_minimize(a, b, c, d, model_sphere_color, plan_complex, model_base)


"""
======================================================================================================
======================= Compute the new plan with the complex number find ============================
======================================================================================================
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
======================= Display Histogram =======================
=========================================================
"""

plt.show()


"""
=====================================================================================
======================= Display model with texture distortion =======================
=====================================================================================
"""

result_angle = abs((model_transform_sphere.face_angles / np.sum(model_transform_sphere.face_angles))
                   - (model_base.face_angles / np.sum(model_base.face_angles)))
result_angle = np.sum(result_angle, axis=1)

result_area = abs((model_transform_sphere.area_faces / np.sum(model_transform_sphere.area_faces))
                  - (model_base.area_faces / np.sum(model_base.area_faces)))


splt.pyglet_plot(model_base, result_angle, plot_colormap=True, caption="Difference angle")
splt.pyglet_plot(model_base, result_area, plot_colormap=True, caption="Difference area")
splt.pyglet_plot(model_transform_sphere, result_area, caption="Difference area")
splt.pyglet_plot(model_transform_sphere,
                 abs(model_transform_sphere.area_faces - model_sphere_color.area_faces),
                 caption="Difference area between model no transfo and model transfo")
