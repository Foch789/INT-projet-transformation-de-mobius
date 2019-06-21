"""@package docstring
Documentation for this module.
More details.
"""

import numpy as np
import matplotlib.pyplot as plt

import slam.distortion as dist


def plot_compare(array_x, array_y, legend="", title="Histogram", label_x="x", label_y="y", display_best_minimum=False,
                 display_best_maximum=False, min_x=None,max_x=None,min_y=None,max_y=None):

    fig, ax = plt.subplots(1, 1)
    ax.set_title(title)
    ax.set_xlabel(label_x)
    ax.set_ylabel(label_y)
    ax.grid(True)
    if legend == "":
        ax.plot(array_x, array_y, 'bo-')
    else:
        ax.plot(array_x, array_y, 'bo-', label=legend)

    if display_best_maximum:
        ax.plot(array_x[array_y.index(max(array_y))], max(array_y), 'ro', label='Best maximum')

    if display_best_minimum:
        ax.plot(array_x[array_y.index(min(array_y))], min(array_y), 'mo', label='Best minimum')

    if max_x is not None:
        plt.xlim(right=max_x)
    if min_x is not None:
        plt.xlim(left=min_x)

    if max_y is not None:
        plt.ylim(top=max_y)
    if min_y is not None:
        plt.ylim(bottom=min_y)

    ax.axvline(x=0, color='k')
    ax.legend()

    plt.show()

    pass


def plot_compare_2_axis_y(array_x, array_y, array_y2,legendy="", legendy2="", title="Histogram", label_x="x", label_y="y",
                          label_y2="y2", display_best_minimum=False, display_best_maximum=False, min_x=None, max_x=None,
                          min_y=None, max_y=None, min_y2=None, max_y2=None):

    fig, ax = plt.subplots(1, 1)
    ax.set_title(title)
    ax.set_xlabel(label_x)
    ax.set_ylabel(label_y)
    ax.grid(True)

    if legendy == "":
        ax.plot(array_x, array_y, 'bo-')
    else:
        ax.plot(array_x, array_y, 'bo-', label=legendy)

    if display_best_maximum:
        ax.plot(array_x[array_y.index(max(array_y))], max(array_y), 'ro', label='Best maximum')

    if display_best_minimum:
        ax.plot(array_x[array_y.index(min(array_y))], min(array_y), 'mo', label='Best minimum')

    if max_x is not None:
        plt.xlim(right=max_x)
    if min_x is not None:
        plt.xlim(left=min_x)

    if max_y is not None:
        plt.ylim(top=max_y)
    if min_y is not None:
        plt.ylim(bottom=min_y)

    ax.axvline(x=0, color='k')
    ax.legend(loc=2)

    ax2 = ax.twinx()
    ax2.set_ylabel(label_y2)
    ax2.plot(array_x, array_y2, 'go-')

    if legendy2 == "":
        ax2.plot(array_x, array_y2, 'go-')
    else:
        ax2.plot(array_x, array_y2, 'go-', label=legendy2)

    if display_best_maximum:
        ax2.plot(array_x[array_y2.index(max(array_y2))], max(array_y2), 'ro', label='Best maximum')

    if display_best_minimum:
        ax2.plot(array_x[array_y2.index(min(array_y2))], min(array_y2), 'mo', label='Best minimum')

    if max_y2 is not None:
        plt.ylim(top=max_y2)
    if min_y2 is not None:
        plt.ylim(bottom=min_y2)

    ax2.legend(loc=0)
    plt.show()

    pass


"""
=====================================================
======================= Angle =======================
=====================================================
"""


def compare_mesh_list_angle(meshs):
    """
        Compare_mesh_list_angle

        Compare all models by their angles with
        the first model to see the distortion (first trismesh of array).
        !!! Use display_plot() for the display of result AND IT'S NOT NORMALIZING !!!
        (display a histogram)

        :param meshs
        :type array [trimesh,trimesh,...]
    """

    mesh1 = meshs[0]
    for i in range(1, len(meshs)):
        angle_diff = dist.angle_difference(mesh1, meshs[i])
        f, ax = plt.subplots(1, 1)
        ax.set_title('angles compare '
                     + mesh1.metadata['name']
                     + " to "
                     + meshs[i].metadata['name'])
        ax.hist(angle_diff.flatten(), 100)
        ax.grid(True)

    pass


def compare_mesh_list_angle_pourcent(meshs):
    """
        compare_mesh_list_area_curve_pourcent

        Compare all models by their angles with
        the first model to see the distortion in pourcent (first trismesh of array).
        !!! Use display_plot() for the display of result !!!
        (Display a curve)

        :param meshs
        :type array [trimesh,trimesh,...]
    """

    mesh1 = meshs[0]
    array_name = []
    array_result = []

    for i in range(1, len(meshs)):
        result = abs((meshs[i].face_angles/np.sum(meshs[i].face_angles))
                     - (mesh1.face_angles/np.sum(mesh1.face_angles)))
        result_result = np.sum(result) * 100
        array_name.append(i)
        array_result.append(result_result)

    names = array_name
    values = array_result

    if len(array_result) != 1:
        fig2, ax2 = plt.subplots(1, 1)
        ax2.plot(names, values, 'ro-')
        ax2.set_title('Angles compare in pourcent curve')
        ax2.set_xlabel('Model to compare')
        ax2.set_ylabel('Angles compare in pourcent')
    else:
        fig2, ax2 = plt.subplots(1, 1)
        plt.bar(array_name, values)
        ax2.set_title('Angles compare in pourcent')
        ax2.set_xlabel('Model to compare')
        ax2.set_ylabel('Angles compare in pourcent')

    print("Average of distortion in pourcent (Angles): "
          + str(np.sum(array_result)/len(array_result))
          + "%")

    return np.sum(array_result) / len(array_result), values


def compare_meshs_angle_median(mesh_base, mesh_compare, histo=False):
    """
            compare_meshs_angle_median

            Compare two models by their angle with
            the mesh_base to see the distortion.
            !!! Use display_plot() for the display of result !!!
            (Display a curve)

            :param mesh_base: mesh of Trimesh

            :param mesh_compare : mesh of Trimesh to compare mesh_base

            :param histo : Display the histogram

            :return value: This a mediane of angle distortion
        """

    result_angle = abs(((mesh_compare.face_angles / np.sum(mesh_compare.face_angles))
                        - (mesh_base.face_angles / np.sum(mesh_base.face_angles))) / (
                                   mesh_base.face_angles / np.sum(mesh_base.face_angles)))
    result_angle = np.sum(result_angle, axis=1)
    result_angle = sorted(result_angle)
    result_result = result_angle[int((len(result_angle) + 1) / 2)]

    names = "mesh_to_compare"
    values = result_result

    if histo:
        fig2, ax2 = plt.subplots(1, 1)
        plt.bar(names, values)
        ax2.set_title('Angles compare (Mediane)')
        ax2.set_xlabel('Model to compare')
        ax2.set_ylabel('Angles distortion mediane')

    print("Distortion angle mediane : "
          + str(values))

    return values


"""
=====================================================
======================= Area ========================
=====================================================
"""


def compare_mesh_list_area(meshs):
    """
        Compare_mesh_angle

        Compare all models by their areas with
        the first model to see the distortion (first trismesh of array).
        !!! Use display_plot() for the display of result AND IT'S NOT NORMALIZING !!!
        (display a histogram)

        :param meshs
        :type array [trimesh,trimesh,...]
    """

    mesh1 = meshs[0]
    for i in range(1, len(meshs)):
        area_diff = dist.area_difference(mesh1, meshs[i])
        f, ax = plt.subplots(1, 1)
        ax.set_title('areas compare '
                     + mesh1.metadata['name']
                     + " to "
                     + meshs[i].metadata['name'])
        ax.hist(area_diff.flatten(), 100)
        ax.grid(True)

    pass


def compare_mesh_list_area_pourcent(meshs):
    """
        compare_mesh_list_area_curve_pourcent

        Compare all models by their areas with
        the first model to see the distortion in pourcent in pourcent (first trismesh of array).
        !!! Use display_plot() for the display of result !!!
        (Display a curve)

        :param meshs
        :type array [trimesh,trimesh,...]
    """

    mesh1 = meshs[0]
    array_name = []
    array_result = []

    for i in range(1, len(meshs)):
        result = abs((meshs[i].area_faces/meshs[i].area)
                     - (mesh1.area_faces/mesh1.area))
        result_result = np.sum(result) * 100
        array_name.append(i)
        array_result.append(result_result)

    names = array_name
    values = array_result

    if len(array_result) != 1:
        fig2, ax2 = plt.subplots(1, 1)
        ax2.plot(names, values, 'ro-')
        ax2.set_title('Areas compare in pourcent curve')
        ax2.set_xlabel('Model to compare')
        ax2.set_ylabel('Areas compare in pourcent')
    else:
        fig2, ax2 = plt.subplots(1, 1)
        plt.bar(array_name, values)
        ax2.set_title('Angles compare in pourcent')
        ax2.set_xlabel('Model to compare')
        ax2.set_ylabel('Angles compare in pourcent')

    print("Average of distortion in pourcent (Areas): "
          + str(np.sum(array_result)/len(array_result))
          + "%")

    return np.sum(array_result) / len(array_result), values
    pass


def compare_meshs_area_median(mesh_base, mesh_compare, histo=False):
    """
            compare_meshs_angle_median

            Compare two models by their areas with
            the mesh_base to see the distortion.
            !!! Use display_plot() for the display of result !!!
            (Display a curve)

            :param mesh_base: mesh of Trimesh

            :param mesh_compare : mesh of Trimesh to compare mesh_base

            :param histo : Display the histogram

            :return value: This a mediane of area distortion
        """

    result_area = abs(((mesh_base.area_faces / np.sum(mesh_base.area_faces))
                       - (mesh_compare.area_faces / np.sum(mesh_compare.area_faces))) / (
                              mesh_compare.area_faces / np.sum(mesh_compare.area_faces)))
    result_area = sorted(result_area)
    result_result = result_area[int((len(result_area) + 1) / 2)]

    names = "mesh_to_compare"
    values = result_result

    if histo:
        fig2, ax2 = plt.subplots(1, 1)
        plt.bar(names, values)
        ax2.set_title('Areas compare (Mediane)')
        ax2.set_xlabel('Model to compare')
        ax2.set_ylabel('Areas distortion mediane')

    print("Distortion area mediane : "
          + str(values))

    return values

"""
============================================================
======================= Edge length ========================
============================================================
"""


def compare_mesh_list_edge_pourcent(meshs):
    """
        compare_mesh_list_edge_pourcent

        Compare all models by their edges with
        the first model to see the distortion in pourcent (first trismesh of array)
        !!! Use display_plot() for the display of result !!!
        (Display a curve)

        :param meshs
        :type array [trimesh,trimesh,...]
    """
    mesh1 = meshs[0]
    array_name = []
    array_result = []
    for i in range(1, len(meshs)):
        result = abs((meshs[i].edges_unique_length
                      / np.sum(meshs[i].edges_unique_length))
                     - (mesh1.edges_unique_length
                        / np.sum(mesh1.edges_unique_length)))
        result_result = np.sum(result) * 100
        array_name.append(i)
        array_result.append(result_result)

    names = array_name
    values = array_result

    if len(array_result) != 1:
        fig2, ax2 = plt.subplots(1, 1)
        ax2.plot(names, values, 'ro-')
        ax2.set_title('Edges compare in pourcent curve')
        ax2.set_xlabel('Model to compare')
        ax2.set_ylabel('Edges compare in pourcent')
    else:
        fig2, ax2 = plt.subplots(1, 1)
        plt.bar(array_name, values)
        ax2.set_title('Angles compare in pourcent')
        ax2.set_xlabel('Model to compare')
        ax2.set_ylabel('Angles compare in pourcent')

    print("Average of distortion in pourcent (Edges length): "
          + str(np.sum(array_result) / len(array_result))
          + "%")

    return np.sum(array_result) / len(array_result), values
    pass


"""
========================================================================
======================= Superimpose the texture ========================
========================================================================
"""


def superimpose_the_texture(mesh1, mesh2):
    """
        superimpose_the_texture

        Take the texture of mesh2 and superimpose on the mesh1

        :param mesh1
        :type trimesh

        :param mesh2
        :type trimesh

        :return new mesh1 with texture
    """

    mesh_copy = mesh1.copy()
    mesh_copy.visual.face_colors = mesh2.visual.face_colors

    return mesh_copy

    pass
