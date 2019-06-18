import slam.io as sio

# Put your path model .gii in array
model = ['../model/foetus/foetus1_sphere.gii',
         '../model/foetus/foetus2_sphere.gii'
         ]

for i in range(0, len(model)):
    mesh_export = sio.load_mesh(model[i])
    mesh_export.export(model[i][:-3]+'ply')
