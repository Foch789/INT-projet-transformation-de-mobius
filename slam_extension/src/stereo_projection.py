__author__ = 'guillaume auzias, guillaume.auzias@gmail.com'

import numpy as np
import os
import matplotlib.pyplot as plt
import nibabel.gifti as ng


def graph_stereo_projection(graph_vertices, graph_center, sphere_radius=None, sphere_center=None):
    """
    compute the stereographic projection of the graph vertices onto the horizontal plane with graph_center at the coordinate [0,0,-1]
    :param graph_vertices: Nx3 coordinates of the vertices (nodes) of the graph onto the sphere
    :param graph_center: 1x3 coordinates of the center or searchlight point onto the sphere
    :param sphere_radius: float, radius of the sphere
    :param sphere_center:  1x3 coordinates of the center of the sphere, if not given then assume the sphere is centered in 0
    :return: Nx3 coordinates of the projected vertices of the graph
    """
    if sphere_center is None:
        sphere_center = [0, 0, 0]
    else:
        graph_vertices -= sphere_center
        graph_center -= sphere_center
    if sphere_radius is None:
        sphere_radius = np.linalg.norm(graph_center)
        print('sphere radius is '+str(sphere_radius) )
    # normalize to be on the unit sphere if necessary
    if sphere_radius is not 1:
        graph_vertices = graph_vertices / sphere_radius
        graph_center = graph_center / sphere_radius
        print(np.mean(graph_vertices, 0))
        print(np.max(graph_vertices, 0))
        print(np.min(graph_vertices, 0))
        print(graph_center)

    # compute the rotation to put the graph center at the coordinate [0, 0, -1]
    rot = rotation(graph_center, [0, 0, -1])

    # rotate the graph vertices
    graph_vertices = np.dot(graph_vertices, rot)
    # compute the stereographic projection
    vert2D = stereo_projection(graph_vertices)
    return vert2D


def stereo_projection(vertices, h=None):
    """
    compute the stereographic projection from the unit sphere (center = 0, radius = 1) onto the horizontal plane which 3rd coordinate is h of the vertices given
    :param vertices: Nx3 coordinates of the vertices to be projected onto the plane
    :param h: 3rd coordinate of the projection plane
    :return: Nx3 coordinates of the vertices projected onto the plane, their 3rd coordinate is thus equal to h
    """
    if h is None:
        h = -1
    for ind, vert in enumerate(vertices):
        vertices[ind, 0] = (-h + 1) * vert[0] / (1 - vert[2])
        vertices[ind, 1] = (-h + 1) * vert[1] / (1 - vert[2])
        vertices[ind, 2] = h
    return vertices


def inverse_stereo_projection(vertices, h=None):
    """
    compute the inverse stereograhic projection from an horizontal plane onto the unit sphere (center = 0, radius = 1)
    :param vertices: Nx3 vertices to be inverse  projected onto the sphere
    :param h: 3rd coordinate of the projection plane
    :return: Nx3 coordinates of the vertices onto the unit sphere
    """
    if h is None:
        h = vertices[0, 2]
    for ind, vert in enumerate(vertices):
        denom = ((1 - h) ** 2 + vert[0] ** 2 + vert[1] ** 2)
        vertices[ind, 2] = (-(1 - h) ** 2 + vert[0] ** 2 + vert[1] ** 2) / denom
        vertices[ind, 1] = 2 * (1 - h) * vert[1] / denom
        vertices[ind, 0] = 2 * (1 - h) * vert[0] / denom
    return vertices


def rotation(src, targ):
    """
    compute the rotation between the two points src and targ onto a sphere centered in 0
    :param src: 3x1 coordinates of the source point onto the sphere
    :param targ: 3x1 coordinates of the target point onto the sphere
    :return:  rot = 3x3 rotation matrix in 3D
    """
    # compute the angle between src and targ
    tet = np.arccos(np.sum((src * targ)) / (np.linalg.norm(src) * np.linalg.norm(targ)))
    # compute the axis arround which the sphere will be rotated = cross product of the vector src and src+targ
    u = np.cross((src + targ), src)
    u = u / np.linalg.norm(u)
    # the rotation is given by the following formula, see e.g. wikipedia rotation matrix ;-)
    c = np.cos(tet)
    s = np.sin(tet)
    rot = np.array([[u[0] ** 2 + (1 - u[0] ** 2) * c, u[0] * u[1] * (1 - c) - u[2] * s, u[0] * u[2] * (1 - c) + u[1] * s], [u[0] * u[1] * (1 - c) + u[2] * s, u[1] ** 2 + (1 - u[1] ** 2) * c, u[1] * u[2] * (1 - c) - u[0] * s], [u[0] * u[2] * (1 - c) - u[1] * s, u[1] * u[2] * (1 - c) + u[0] * s, u[2] ** 2 + (1 - u[2] ** 2) * c]])
    return rot


if __name__ == '__main__':
    file_mesh = '/hpc/crise/takerkart/grabbr/sanlm_fs_db/grabbr_10/surf/gifti/rh.sphere.reg.gii'

    mesh = ng.read(file_mesh)
    vert = mesh.darrays[0].data
    poly = mesh.darrays[1].data
    # mesh = aims.read(file_mesh)
    # vert = np.array(mesh.vertex())
    searchlight = vert[50, :]
    graph_vertices = vert
    print(np.mean(vert, 0))
    print(np.max(vert, 0))
    print(np.min(vert, 0))

    vert2D = graph_stereo_projection(graph_vertices,  searchlight)
    print(vert2D.shape)
    #poly = np.array(mesh.polygon())

    plt.figure()
    plt.gca().set_aspect('equal')
    plt.triplot(vert2D[:, 0], vert2D[:, 1], poly, 'go-')

    # #vert2D[:, 0] = vert2D[:, 0] + 3
    # vert3D = inverse_stereo_projection(vert2D)
    # vv = aims.vector_POINT3DF()
    # for v in vert3D:
    #     vv.append(v)
    # mesh.vertex().assign(vv)
    # mesh.updateNormals()
    # #aims.write(mesh, '/home/toz/stereo.gii')

    plt.show()
