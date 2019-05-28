import trimesh

import slam.io as sio

model = ['../model/foetus/foetus1_sphere.ply',
         '../model/foetus/foetus2_sphere.ply'
         ]

#EN PLY
# for i in range(0, len(model)):
#     mesh_export = sio.load_mesh(model[i])
#     mesh_export.export(model[i][:-3]+'ply')

#EN GII
for i in range(0, len(model)):
    model_path = model[i]
    model_export = trimesh.load(model_path)
    model_export.show()
    sio.write_mesh(model_export, model[i][:-3]+'gii')

