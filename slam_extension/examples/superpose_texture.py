import trimesh
import src.model_treatment as mt

import slam.plot as splt


model_path = '../model/foetus/foetus1.ply'
model_path2 = '../model/foetus/foetus2.ply'
model_sphere_path1 = '../model/foetus/foetus_sphere1.cmcf.ply'
model_register = '../model/foetus/foetus_register.ply'


model = trimesh.load(model_path)
model_sphere = trimesh.load(model_sphere_path1)

model2 = trimesh.load(model_path2)
model_register_mesh = trimesh.load(model_register)

# display_model(model)
# display_model(model_sphere)

# model_result = mt.superimpose_the_texture(model, model_sphere)

splt.pyglet_plot(model)
splt.pyglet_plot(model2)
splt.pyglet_plot(model_register_mesh)
