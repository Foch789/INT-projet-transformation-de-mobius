import trimesh
import src.model_treatment as mt


model_path = '../model/foetus/foetus1.ply'
model_sphere_path = '../model/foetus/foetus_sphere1.cmcf.ply'


model = trimesh.load(model_path)
model_sphere = trimesh.load(model_sphere_path)

# display_model(model)
# display_model(model_sphere)

model_result = mt.superimpose_the_texture(model, model_sphere)

mt.display_model(model_result)
