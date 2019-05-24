import slam.io as sio

model = []

for i in range(0, len(model)):
    mesh_export = sio.load_mesh(model[i])
    mesh_export.export(model[i][:-3]+'ply')
