import trimesh
import src.compare_model as mt

import slam.plot as splt


model_path = '../model/foetus/foetus1.ply'
model_sphere_path = '../model/foetus/foetus1_sphere.ply'


model = trimesh.load(model_path)
model_sphere = trimesh.load(model_sphere_path)


model_result = mt.superimpose_the_texture(model, model_sphere)

splt.pyglet_plot(model, caption="Foetus")
splt.pyglet_plot(model_sphere, caption="Sphere of the foetus")
splt.pyglet_plot(model_result, caption="Texture of the sphere on the foetus")
