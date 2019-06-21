import numpy as np
from scipy.optimize import minimize
from scipy.optimize import dual_annealing

import trimesh
import matplotlib.pyplot as plt

import slam.plot as splt

from slam_extension.src import transformation_sphere as ts
import slam_extension.src.compare_model as cp
import slam_extension.src.stereo_projection as sp
import slam.distortion as sd

models = ['../model/foetus/foetus1.ply',
          '../model/foetus/foetus1_sphere.ply',
          '../model/brain/brain.ply',
          '../model/brain/brain_sphere_100_iters.ply']

model_base = trimesh.load(models[0])  # Foetus
model_sphere = trimesh.load(models[1])  # Foetus sphere

radius_of_sphere = ts.get_radius(model_sphere)

print("radius = " + str(radius_of_sphere))

print("vertices min = " + str(np.amin(model_sphere.vertices, axis=0)))
print("vertices max = " + str(np.amax(model_sphere.vertices, axis=0)))

model_sphere_color = model_sphere.copy()

# Display the sphere with color (Red = North / Blue = South)
splt.pyglet_plot(model_sphere_color, model_sphere_color.vertices[:, 2], caption="Sphere")

plan_sphere = sp.stereo_projection(model_sphere_color.vertices.copy())

# Load the new model Trimesh with the new vertices and color of the sphere.
plan_sphere_visu = trimesh.Trimesh(vertices=plan_sphere,
                                   faces=model_sphere_color.faces.copy(),
                                   vertex_colors=model_sphere_color.visual.vertex_colors.copy(),
                                   process=False)

# Display the plan of the sphere
# splt.pyglet_plot(plan_sphere_visu, caption="Plan sphere")

plan_complex = plan_sphere[:, 0] + (1.0j * plan_sphere[:, 1])


"""
================================================================================
======================= test translate complex param "a"  =======================
================================================================================
"""

angle_array, area_array = ts.translate_a(model_sphere_color, plan_complex, model_base, step=0.1,
                                         iteration=50)

plt.show()

print(area_array[len(area_array)-1][0][0])

res = [area_array[len(area_array)-1][0][0][0],
       area_array[len(area_array)-1][0][0][1],
       area_array[len(area_array)-1][0][0][2],
       area_array[len(area_array)-1][0][0][3]]

#plan_complex_transfo = ts.mobius_transformation(res[0], res[1], res[2], res[3], plan_complex)
plan_complex_transfo = ts.mobius_transformation(complex(1.5, 0.), complex(0., 0.), complex(0., 0.), complex(1., 0.), plan_complex)

real_array = plan_complex_transfo[:].real
imag_array = plan_complex_transfo[:].imag

result_plan_complex = []
for i in range(0, len(real_array)):
    result_plan_complex.append(np.array([real_array[i], imag_array[i], -1]))

result_plan_complex = np.array(result_plan_complex)

new_vertices_sphere = sp.inverse_stereo_projection(result_plan_complex)

model_transform_sphere = trimesh.Trimesh(vertices=new_vertices_sphere,
                                         faces=model_sphere_color.faces,
                                         vertex_colors=model_sphere_color.visual.vertex_colors,
                                         process=False)
print('mean angle dist='+str(np.mean(sd.angle_difference(mesh1=model_transform_sphere, mesh2=model_base))))
print('area dist='+str(np.median(sd.area_difference(mesh1=model_transform_sphere, mesh2=model_base))))

cp.compare_meshs_angle_median(model_base, model_transform_sphere)
cp.compare_meshs_area_median(model_base, model_transform_sphere)

splt.pyglet_plot(model_transform_sphere)

"""
===========================================================================================
======================= Test with algo to reduce that =====================================
===========================================================================================
"""


res = ts.random_complex_median(model_transform_sphere, plan_complex, model_base, min_random=-2,
                               max_random=2, nbr_iteration=1000)

print(res)

plan_complex_transfo = ts.mobius_transformation(res[0], res[1], res[2], res[3], plan_complex)

real_array = plan_complex_transfo[:].real
imag_array = plan_complex_transfo[:].imag

result_plan_complex = []
for i in range(0, len(real_array)):
    result_plan_complex.append(np.array([real_array[i], imag_array[i], -1]))

result_plan_complex = np.array(result_plan_complex)

new_vertices_sphere = sp.inverse_stereo_projection(result_plan_complex)
model_transform_sphere = trimesh.Trimesh(vertices=new_vertices_sphere,
                                         faces=model_sphere_color.faces,
                                         vertex_colors=model_sphere_color.visual.vertex_colors,
                                         process=False)
splt.pyglet_plot(model_transform_sphere)

cp.compare_meshs_angle_median(model_base, model_transform_sphere)
cp.compare_meshs_area_median(model_base, model_transform_sphere)

plt.show()