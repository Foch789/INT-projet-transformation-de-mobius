import trimesh
import slam.io as sio

# Put your path model .ply in array
model = ['../model/foetus/foetus1_sphere.ply',
         '../model/foetus/foetus2_sphere.ply'
         ]

for i in range(0, len(model)):
    model_path = model[i]
    model_export = trimesh.load(model_path)
    model_export.show()
    sio.write_mesh(model_export, model[i][:-3]+'gii')

