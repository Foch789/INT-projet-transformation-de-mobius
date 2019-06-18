import trimesh

import src.compare_model as mt


def test_compare_mesh_list_angle():
    model_path = '../model/foetus/foetus1.ply'
    model_sphere_path = '../model/foetus/foetus_sphere1.cmcf.ply'

    model = trimesh.load(model_path)
    model_sphere = trimesh.load(model_sphere_path)

    brain_transform = mt.superimpose_the_texture(model, model_sphere)

    assert isinstance(brain_transform, trimesh)

    pass
