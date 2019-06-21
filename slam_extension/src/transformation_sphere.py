import numpy as np
from random import *
import matplotlib.pyplot as plt
import matplotlib
import trimesh
import math
from scipy.optimize import minimize

import src.stereo_projection as sp
import src.compare_model as cp

import slam.distortion as sd


def real_to_complex(z):      # real vector of length 2n -> complex of length n
    return z[:len(z)//2] + 1j * z[len(z)//2:]


def complex_to_real(z):      # complex vector of length n -> real of length 2n
    return np.concatenate((np.real(z), np.imag(z)))


def mobius_transformation(a, b, c, d, array_complex):
    """
            mobius_transformation

            Using to transform the plan with complex number.
            (Translate / rotate the plan)

            :param a: Complex number or Integer

            :param b: Complex number or Integer

            :param c: Complex number or Integer

            :param d: Complex number or Integer

            :param array_complex: This array represent the complex plan.
            :type array_complex: array[complex_number]

    """
    numerator = (a * array_complex) + b
    denominator = (c * array_complex) + d

    result = numerator / denominator

    return result


def transform_plan_complexe_to_3d_plan(plan_complex):

    real_array = plan_complex[:].real
    imag_array = plan_complex[:].imag

    result_plan_complex = []
    for p in range(0, len(real_array)):
        result_plan_complex.append(np.array([real_array[p], imag_array[p], -1]))

    return result_plan_complex


"""
=====================================================
======================= Radius ======================
=====================================================
"""


def get_radius(sphere):

    A = np.sum(sphere.area_faces)

    radius = math.sqrt(A/(4*math.pi))

    return radius


"""
=====================================================
======================= Mediane =====================
=====================================================
"""


def get_mediane(array):
    array_return = array.copy()
    array_return = sorted(array_return)
    result = array_return[int((len(array_return) + 1) / 2)]
    return result


"""
=====================================================
======================= Average =====================
=====================================================
"""


def get_average(array):
    array_return = array.copy()
    result = np.sum(array_return)/len(array_return)
    return result


"""
==========================================================
======================= Absolute value ===================
==========================================================
"""


def get_absolute_value_array(array_compare, array_base):
    result_array = abs(array_compare - array_base)
    return result_array


"""
=====================================================
======================= Normalize ===================
=====================================================
"""


def get_array_normalize(array):
    result_array = array.copy()
    result_array = result_array / np.sum(result_array)
    return result_array


"""
=====================================================================
======================= Func for minimize  ==========================
=====================================================================
"""


def func_for_minimize(x, plan_complex, model_sphere_color, model_base, array_angle_result=None, array_area_result=None):
    """
            func_for_minimize

            This func is use by minimize.

            :param x: see https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
            the part x0

            :param plan_complex: This array represent the complex plan.
            :type plan_complex: array[complex_number]

            :param model_sphere_color: Sphere with texture color
            :type model_sphere_color: Trimesh

            :param model_base: Base model (Example the Foetus)
            :type model_base: Trimesh

            :param array_angle_result: This array want the result to the angle (in pourcent).
            :type array_angle_result: array[float]

            :param array_area_result: This array want the result to the area (in pourcent).
            :type array_area_result: array[float]

            :return result_area_pourcent: The area distortion in pourcent.

    """
    a = real_to_complex(x)[0]
    b = real_to_complex(x)[1]
    c = real_to_complex(x)[2]
    d = real_to_complex(x)[3]

    plan_complex_transfo = mobius_transformation(a, b, c, d, plan_complex)

    real_array = plan_complex_transfo[:].real
    imag_array = plan_complex_transfo[:].imag

    result_plan_complex = []
    for p in range(0, len(real_array)):
        result_plan_complex.append(np.array([real_array[p], imag_array[p], -1]))

    result_plan_complex = np.array(result_plan_complex)

    new_vertices_sphere = sp.inverse_stereo_projection(result_plan_complex)
    model_transform_sphere = trimesh.Trimesh(vertices=new_vertices_sphere,
                                             faces=model_sphere_color.faces,
                                             vertex_colors=model_sphere_color.visual.vertex_colors,
                                             process=False)

    result_angle = abs((model_transform_sphere.face_angles / np.sum(model_transform_sphere.face_angles))
                       - (model_base.face_angles / np.sum(model_base.face_angles)))
    result_angle_pourcent = np.sum(result_angle) * 100

    if array_angle_result is not None:
        array_angle_result.append(result_angle_pourcent)

    result_area = abs((model_transform_sphere.area_faces / np.sum(model_transform_sphere.area_faces))
                      - (model_base.area_faces / np.sum(model_base.area_faces)))
    result_area_pourcent = np.sum(result_area) * 100

    if array_area_result is not None:
        array_area_result.append(result_area_pourcent)

    return result_area_pourcent


"""
=====================================================================
======================= Func random_complex  ========================
=====================================================================
"""


def random_complex_median(model_sphere_color, plan_complex, model_base, min_random=-100, max_random=100, nbr_iteration=500):
    """
            random_complex_median

            This function create by Laurent DOITEAU.
            Try to find the best parameter to reduce the area distortion.
            Display the mediane ( Don't forget plot.show())

            :param model_sphere_color: Sphere with texture color
            :type model_sphere_color: Trimesh

            :param plan_complex: This array represent the complex plan.
            :type plan_complex: array[complex_number]

            :param model_base: Base model (Example the Foetus)
            :type model_base: Trimesh

            :param min_random: The minimum for the interval random.
            :type min_random: Integer

            :param max_random: The maximum for the interval random.
            :type max_random: Integer

            :param nbr_iteration: The numbers of iterations to find the best parameters
            :type nbr_iteration: Integer

            :return The best parameter find by this function.

    """
    result_all_angle = []
    result_all_area = []
    array_name = []
    array_complex_number = []

    save_best_iteration_area = 0
    min_area = 1000000000.0

    save_best_iteration_angle = 0
    min_angle = 1000000000.0

    best_iteration = 0
    score = 1000000000.0

    nbrAMin = min_random
    nbrAMax = max_random
    nbrAMin_IMAG = min_random
    nbrAMax_IMAG = max_random

    nbrBMin = min_random
    nbrBMax = max_random
    nbrBMin_IMAG = min_random
    nbrBMax_IMAG = max_random

    nbrCMin = min_random
    nbrCMax = max_random
    nbrCMin_IMAG = min_random
    nbrCMax_IMAG = max_random

    nbrDMin = min_random
    nbrDMax = max_random
    nbrDMin_IMAG = min_random
    nbrDMax_IMAG = max_random

    for i in range(1, nbr_iteration):

        a = complex(uniform(nbrAMin, nbrAMax), uniform(nbrAMin_IMAG, nbrAMax_IMAG))
        b = complex(uniform(nbrBMin, nbrBMax), uniform(nbrBMin_IMAG, nbrBMax_IMAG))
        c = complex(uniform(nbrCMin, nbrCMax), uniform(nbrCMin_IMAG, nbrCMax_IMAG))
        d = complex(uniform(nbrDMin, nbrDMax), uniform(nbrDMin_IMAG, nbrDMax_IMAG))

        array_name.append(i)
        array_complex_number.append([a, b, c, d])

        plan_complex_transfo = mobius_transformation(a, b, c, d, plan_complex)

        result_plan_complex = transform_plan_complexe_to_3d_plan(plan_complex_transfo)
        result_plan_complex = np.array(result_plan_complex)

        new_vertices_sphere = sp.inverse_stereo_projection(result_plan_complex)
        model_transform_sphere = trimesh.Trimesh(vertices=new_vertices_sphere,
                                                 faces=model_sphere_color.faces,
                                                 vertex_colors=model_sphere_color.visual.vertex_colors,
                                                 process=False)

        result_angle = sd.angle_difference(model_transform_sphere, model_base)
        result_angle = np.sum(result_angle, axis=1)
        result_angle_mediane = get_mediane(result_angle)
        result_all_angle.append(result_angle_mediane)

        model_transform_sphere_area_norm = get_array_normalize(model_transform_sphere.area_faces)
        model_base_area_norm = get_array_normalize(model_base.area_faces)

        result_area = get_absolute_value_array(model_transform_sphere_area_norm, model_base_area_norm) / model_base_area_norm
        result_area_mediane = get_mediane(result_area)
        result_all_area.append(result_area_mediane)

        if min_angle > result_angle_mediane:
            min_angle = result_angle_mediane
            save_best_iteration_angle = i

        if min_area > result_area_mediane:
            save_best_iteration_area = i
            min_area = result_area_mediane

        if score > result_area_mediane + result_angle_mediane:
            score = result_area_mediane + result_angle_mediane
            best_iteration = i
            if a.real >= 0:
                nbrAMax = a.real
            else:
                nbrAMin = a.real
            if a.imag >= 0:
                nbrAMax_IMAG = a.imag
            else:
                nbrAMin_IMAG = a.imag

            if b.real >= 0:
                nbrBMax = b.real
            else:
                nbrBMin = b.real
            if b.imag >= 0:
                nbrBMax_IMAG = b.imag
            else:
                nbrBMin_IMAG = b.imag

            if c.real >= 0:
                nbrCMax = c.real
            else:
                nbrCMin = c.real
            if c.imag >= 0:
                nbrCMax_IMAG = c.imag
            else:
                nbrCMin_IMAG = c.imag

            if d.real >= 0:
                nbrDMax = d.real
            else:
                nbrDMin = d.real
            if d.imag >= 0:
                nbrDMax_IMAG = d.imag
            else:
                nbrDMin_IMAG = d.imag

    print("See the best score general angle "
          + str(result_all_angle[best_iteration - 1]))

    print("See the best score general area "
          + str(result_all_area[best_iteration - 1]))

    return array_complex_number[best_iteration-1]


"""
====================================================================
======================= Func algo_minimize  ========================
====================================================================
"""


def algo_minimize(a, b, c, d, func, model_sphere_color, plan_complex, model_base):
    """
            algo_minimize

            This function use minimize of scipy.optimize and it will find the best complex
            parameter to reduce the distortions.

            :param a: Complex number

            :param b: Complex number

            :param c: Complex number

            :param d: Complex number

            :param model_sphere_color: Sphere with texture color
            :type model_sphere_color: Trimesh

            :param plan_complex: This array represent the complex plan.
            :type plan_complex: array[complex_number]

            :param model_base: Base model (Example the Foetus)
            :type model_base: Trimesh

            :return The best parameter find by this function.

    """
    print(complex_to_real([a, b, c, d]))

    array_area_result = []
    array_angle_result = []

    res = minimize(func_for_minimize,
                   complex_to_real([a, b, c, d]),
                   args=(plan_complex, model_sphere_color, model_base, array_angle_result, array_area_result),
                   method='Nelder-Mead',
                   options={'disp': True})

    res = real_to_complex(res.x)

    array_name_minimize = []

    for i in range(1, len(array_area_result)+1):
        array_name_minimize.append(i)

    fig, ax = plt.subplots(1, 1)
    ax.set_title('Distorsion evolution')
    ax.set_xlabel('Number of tests')
    ax.set_ylabel('% distorsion')

    ax.plot(array_name_minimize, array_angle_result, 'go-', label='angle evolution')
    ax.plot(array_name_minimize[0], array_angle_result[0], 'yo')
    ax.plot(array_angle_result.index(min(array_angle_result)), min(array_angle_result), 'ro')

    ax.plot(array_name_minimize, array_area_result, 'bo-', label='area evolution')
    ax.plot(array_name_minimize[0], array_area_result[0], 'yo')
    ax.plot(array_area_result.index(min(array_area_result)), min(array_area_result), 'ro',
            label='minimum distortion')
    ax.legend()

    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')

    print("See the best score for angle with "
          + str(min(array_angle_result)) + "%")

    print("See the best score for area with "
          + str(min(array_area_result)) + "%")

    return res


"""
===========================================================================
======================= Func change one parameter  ========================
===========================================================================
"""


def translate_a(model_sphere_color, plan_complex, model_base,
                           b=complex(0., 0.),
                           c=complex(0., 0.),
                           d=complex(1., 0.),
                           pas=1,
                           iteration=100):
    """
            translate_a

            This function try all variant for parameter a with his angle.

            :param model_sphere_color: Sphere with texture color
            :type model_sphere_color: Trimesh

            :param plan_complex: This array represent the complex plan.
            :type plan_complex: array[complex_number]

            :param model_base: Base model (Example the Foetus)
            :type model_base: Trimesh

            :param b: Complex number or Integer (parameter to transform the plan)
            :type b: Complex or Integer

            :param c: Complex number or Integer (parameter to transform the plan)
            :type c: Complex or Integer

            :param d: Complex number or Integer (parameter to transform the plan)
            :type d: Complex or Integer

            :param pas: step to modify the parameter a

            :param iteration: Number of iterations

            :return The best parameter find by this function.

    """
    result_all_angle = [[], []]
    result_all_angle_complex = []
    result_all_angle_value = []
    result_all_area = [[], []]
    result_all_area_complex = []
    result_all_area_value = []
    array_name = []

    t = 0

    angle_first_value = sd.angle_difference(mesh1=model_sphere_color, mesh2=model_base)
    angle_first_value = np.sum(angle_first_value, axis=1)
    angle_first_value = get_average(angle_first_value)
    area_first_value = cp.compare_meshs_area_median(model_base, model_sphere_color)

    array_name.append(t)

    result_all_angle_complex.append([0, 0, 0, 0])
    result_all_angle_value.append(angle_first_value)

    result_all_area_complex.append([0, 0, 0, 0])
    result_all_area_value.append(area_first_value * 100)

    for i in range(0, iteration):

        t += pas
        array_name.append(t)
        a = complex(t, t)

        plan_complex_transfo = mobius_transformation(a, b, c, d, plan_complex)

        result_plan_complex = transform_plan_complexe_to_3d_plan(plan_complex_transfo)
        result_plan_complex = np.array(result_plan_complex)

        new_vertices_sphere = sp.inverse_stereo_projection(result_plan_complex)
        model_transform_sphere = trimesh.Trimesh(vertices=new_vertices_sphere,
                                                 faces=model_sphere_color.faces,
                                                 vertex_colors=model_sphere_color.visual.vertex_colors,
                                                 process=False)

        result_angle = sd.angle_difference(mesh1=model_transform_sphere, mesh2=model_base)
        result_angle = np.sum(result_angle, axis=1)
        result_angle_mediane = get_average(result_angle)

        model_transform_sphere_area_norm = get_array_normalize(model_transform_sphere.area_faces)
        model_base_area_norm = get_array_normalize(model_base.area_faces)

        result_area = get_absolute_value_array(model_transform_sphere_area_norm, model_base_area_norm) / model_base_area_norm
        result_area_mediane = get_mediane(result_area) * 100

        result_all_angle_complex.append([a, b, c, d])
        result_all_angle_value.append(result_angle_mediane)

        result_all_area_complex.append([a, b, c, d])
        result_all_area_value.append(result_area_mediane)

    cp.plot_compare_2_axis_y(array_name, result_all_area_value, result_all_angle_value, legendy="Area evolution",
                             legendy2="Angle evolution", title="Distortion evolution mediane for parameter a",
                             label_x="Step " + str(pas) + " of a",  label_y="Distortion mm² (mediane) %",
                             label_y2="Distortion angle average", display_best_minimum=True, display_best_maximum=True,
                             min_y2=np.pi * -1, max_y2=np.pi)

    result_all_angle_complex.pop(0)
    result_all_angle_value.pop(0)

    result_all_area_complex.pop(0)
    result_all_area_value.pop(0)

    result_all_angle.append([result_all_angle_complex, result_all_angle_value])
    result_all_area.append([result_all_area_complex, result_all_area_value])

    return result_all_angle, result_all_area


"""
=============================================================================================
======================= Func random_complex_with_minimize (obsolete) ========================
=============================================================================================
"""

# (obsolete)


def random_complex_with_minimize(model_sphere_color, plan_complex, model_base, min_random=-100, max_random=100,
                                 nbr_iteration=10):
    """
            random_complex_with_minimize

            This function create by Laurent DOITEAU.
            Try to find the best parameter to reduce the area distortion.
            With minimize !

            :param model_sphere_color: Sphere with texture color
            :type model_sphere_color: Trimesh

            :param plan_complex: This array represent the complex plan.
            :type plan_complex: array[complex_number]

            :param model_base: Base model (Example the Foetus)
            :type model_base: Trimesh

            :param min_random: The minimum for the interval random.
            :type min_random: Integer

            :param max_random: The maximum for the interval random.
            :type max_random: Integer

            :param nbr_iteration: The numbers of iterations to find the best parameters
            :type nbr_iteration: Integer

            :return The best parameter find by this function.

    """
    result_all_angle = []
    result_all_area = []
    array_name = []
    array_result = []

    save_best_iteration_angle = 0
    min_angle = 1000000000.0

    save_best_iteration_area = 0
    min_area = 1000000000.0

    nbrAMin = min_random
    nbrAMax = max_random
    nbrAMin_IMAG = min_random
    nbrAMax_IMAG = max_random

    nbrBMin = min_random
    nbrBMax = max_random
    nbrBMin_IMAG = min_random
    nbrBMax_IMAG = max_random

    nbrCMin = min_random
    nbrCMax = max_random
    nbrCMin_IMAG = min_random
    nbrCMax_IMAG = max_random

    nbrDMin = min_random
    nbrDMax = max_random
    nbrDMin_IMAG = min_random
    nbrDMax_IMAG = max_random

    for i in range(1, nbr_iteration):

        a = complex(uniform(nbrAMin, nbrAMax), uniform(nbrAMin_IMAG, nbrAMax_IMAG))
        b = complex(uniform(nbrBMin, nbrBMax), uniform(nbrBMin_IMAG, nbrBMax_IMAG))
        c = complex(uniform(nbrCMin, nbrCMax), uniform(nbrCMin_IMAG, nbrCMax_IMAG))
        d = complex(uniform(nbrDMin, nbrDMax), uniform(nbrDMin_IMAG, nbrDMax_IMAG))

        array_name.append(i)

        res = minimize(func_for_minimize,
                       complex_to_real([a, b, c, d]),
                       args=(plan_complex, model_sphere_color, model_base),
                       method='Nelder-Mead',
                       options={'disp': True})

        res = real_to_complex(res.x)

        array_result.append([res[0], res[1], res[2], res[3]])

        plan_complex_transfo = mobius_transformation(res[0], res[1], res[2], res[3], plan_complex)

        real_array = plan_complex_transfo[:].real
        imag_array = plan_complex_transfo[:].imag

        result_plan_complex = []
        for p in range(0, len(real_array)):
            result_plan_complex.append(np.array([real_array[p], imag_array[p], -1]))

        result_plan_complex = np.array(result_plan_complex)

        new_vertices_sphere = sp.inverse_stereo_projection(result_plan_complex)
        model_transform_sphere = trimesh.Trimesh(vertices=new_vertices_sphere,
                                                 faces=model_sphere_color.faces,
                                                 vertex_colors=model_sphere_color.visual.vertex_colors,
                                                 process=False)

        result_angle = abs((model_transform_sphere.face_angles / np.sum(model_transform_sphere.face_angles))
                           - (model_base.face_angles / np.sum(model_base.face_angles)))
        result_angle_pourcent = np.sum(result_angle) * 100
        result_all_angle.append(result_angle_pourcent)

        result_area = abs((model_transform_sphere.area_faces / np.sum(model_transform_sphere.area_faces))
                          - (model_base.area_faces / np.sum(model_base.area_faces)))
        result_area_pourcent = np.sum(result_area) * 100
        result_all_area.append(result_area_pourcent)

        if min_angle > result_angle_pourcent:
            min_angle = result_angle_pourcent
            save_best_iteration_angle = i

        if min_area > result_area_pourcent:
            save_best_iteration_area = i
            min_area = result_area_pourcent

            if a.real >= 0:
                nbrAMax = a.real
            else:
                nbrAMin = a.real
            if a.imag >= 0:
                nbrAMax_IMAG = a.imag
            else:
                nbrAMin_IMAG = a.imag

            if b.real >= 0:
                nbrBMax = b.real
            else:
                nbrBMin = b.real
            if b.imag >= 0:
                nbrBMax_IMAG = b.imag
            else:
                nbrBMin_IMAG = b.imag

            if c.real >= 0:
                nbrCMax = c.real
            else:
                nbrCMin = c.real
            if c.imag >= 0:
                nbrCMax_IMAG = c.imag
            else:
                nbrCMin_IMAG = c.imag

            if d.real >= 0:
                nbrDMax = d.real
            else:
                nbrDMin = d.real
            if d.imag >= 0:
                nbrDMax_IMAG = d.imag
            else:
                nbrDMin_IMAG = d.imag

    fig, ax = plt.subplots(1, 1)
    plt.bar(array_name, result_all_angle)
    ax.set_title('Distorsion angle evolution (of complex a)')
    ax.set_xlabel('Number of tests')
    ax.set_ylabel('% distorsion angle')
    ax.plot(array_name, result_all_angle, 'r-')

    fig, ax = plt.subplots(1, 1)
    plt.bar(array_name, result_all_area)
    ax.set_title('Distorsion area evolution')
    ax.set_xlabel('Number of tests')
    ax.set_ylabel('% distorsion area')
    ax.plot(array_name, result_all_area, 'r-')

    fig, ax = plt.subplots(1, 1)
    ax.set_title('Distorsion evolution')
    ax.set_xlabel('Number of tests')
    ax.set_ylabel('% distorsion')

    ax.plot(array_name, result_all_angle, 'go-', label='angle evolution')
    ax.plot(array_name[0], result_all_angle[0], 'yo')
    ax.plot(array_name[save_best_iteration_angle - 1], result_all_angle[save_best_iteration_angle - 1], 'ro')

    ax.plot(array_name, result_all_area, 'bo-', label='area evolution')
    ax.plot(array_name[0], result_all_area[0], 'yo')
    ax.plot(array_name[save_best_iteration_area - 1], result_all_area[save_best_iteration_area - 1], 'ro',
            label='minimum distortion')

    ax.legend()

    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')

    print("See the best score for area (" + str(save_best_iteration_area) + " iteration) with "
          + str(result_all_area[save_best_iteration_area - 1]) + "%")

    return array_result[save_best_iteration_area - 1]


def random_complex_average(model_sphere_color, plan_complex, model_base, min_random=-100, max_random=100, nbr_iteration=500):
    """
            random_complex_average

            This function create by Laurent DOITEAU.
            Try to find the best parameter to reduce the area distortion.

            :param model_sphere_color: Sphere with texture color
            :type model_sphere_color: Trimesh

            :param plan_complex: This array represent the complex plan.
            :type plan_complex: array[complex_number]

            :param model_base: Base model (Example the Foetus)
            :type model_base: Trimesh

            :param min_random: The minimum for the interval random.
            :type min_random: Integer

            :param max_random: The maximum for the interval random.
            :type max_random: Integer

            :param nbr_iteration: The numbers of iterations to find the best parameters
            :type nbr_iteration: Integer

            :return The best parameter find by this function.

    """
    result_all_angle = []
    result_all_area = []
    array_name = []
    array_complex_number = []

    save_best_iteration_area = 0
    min_area = 1000000000.0

    save_best_iteration_angle = 0
    min_angle = 1000000000.0

    best_iteration = 0
    score = 1000000000.0

    nbrAMin = min_random
    nbrAMax = max_random
    nbrAMin_IMAG = min_random
    nbrAMax_IMAG = max_random

    nbrBMin = min_random
    nbrBMax = max_random
    nbrBMin_IMAG = min_random
    nbrBMax_IMAG = max_random

    nbrCMin = min_random
    nbrCMax = max_random
    nbrCMin_IMAG = min_random
    nbrCMax_IMAG = max_random

    nbrDMin = min_random
    nbrDMax = max_random
    nbrDMin_IMAG = min_random
    nbrDMax_IMAG = max_random

    for i in range(1, nbr_iteration):

        a = complex(uniform(nbrAMin, nbrAMax), uniform(nbrAMin_IMAG, nbrAMax_IMAG))
        b = complex(uniform(nbrBMin, nbrBMax), uniform(nbrBMin_IMAG, nbrBMax_IMAG))
        c = complex(uniform(nbrCMin, nbrCMax), uniform(nbrCMin_IMAG, nbrCMax_IMAG))
        d = complex(uniform(nbrDMin, nbrDMax), uniform(nbrDMin_IMAG, nbrDMax_IMAG))

        array_name.append(i)
        array_complex_number.append([a, b, c, d])

        plan_complex_transfo = mobius_transformation(a, b, c, d, plan_complex)

        real_array = plan_complex_transfo[:].real
        imag_array = plan_complex_transfo[:].imag

        result_plan_complex = []
        for p in range(0, len(real_array)):
            result_plan_complex.append(np.array([real_array[p], imag_array[p], -1]))

        result_plan_complex = np.array(result_plan_complex)

        new_vertices_sphere = sp.inverse_stereo_projection(result_plan_complex)
        model_transform_sphere = trimesh.Trimesh(vertices=new_vertices_sphere,
                                                 faces=model_sphere_color.faces,
                                                 vertex_colors=model_sphere_color.visual.vertex_colors,
                                                 process=False)

        result_angle = abs(((model_transform_sphere.face_angles / np.sum(model_transform_sphere.face_angles))
                           - (model_base.face_angles / np.sum(model_base.face_angles)))/(model_base.face_angles / np.sum(model_base.face_angles)))
        result_angle_pourcent = (np.sum(result_angle)/len(result_angle))
        result_all_angle.append(result_angle_pourcent)

        result_area = abs(((model_transform_sphere.area_faces / np.sum(model_transform_sphere.area_faces))
                          - (model_base.area_faces / np.sum(model_base.area_faces)))/(model_base.area_faces / np.sum(model_base.area_faces)))
        result_area_pourcent = (np.sum(result_area)/len(result_area))
        result_all_area.append(result_area_pourcent)

        if min_angle > result_angle_pourcent:
            min_angle = result_angle_pourcent
            save_best_iteration_angle = i

        if min_area > result_area_pourcent:
            save_best_iteration_area = i
            min_area = result_area_pourcent

        if score > result_area_pourcent + result_angle_pourcent:
            score = result_area_pourcent + result_angle_pourcent
            best_iteration = i
            if a.real >= 0:
                nbrAMax = a.real
            else:
                nbrAMin = a.real
            if a.imag >= 0:
                nbrAMax_IMAG = a.imag
            else:
                nbrAMin_IMAG = a.imag

            if b.real >= 0:
                nbrBMax = b.real
            else:
                nbrBMin = b.real
            if b.imag >= 0:
                nbrBMax_IMAG = b.imag
            else:
                nbrBMin_IMAG = b.imag

            if c.real >= 0:
                nbrCMax = c.real
            else:
                nbrCMin = c.real
            if c.imag >= 0:
                nbrCMax_IMAG = c.imag
            else:
                nbrCMin_IMAG = c.imag

            if d.real >= 0:
                nbrDMax = d.real
            else:
                nbrDMin = d.real
            if d.imag >= 0:
                nbrDMax_IMAG = d.imag
            else:
                nbrDMin_IMAG = d.imag

    fig, ax = plt.subplots(1, 1)
    ax.set_title('Distortion evolution mediane')
    ax.set_xlabel('Number of tests')
    ax.set_ylabel('Distortion mm² (mediane)')

    ax.plot(array_name, result_all_angle, 'go-', label='angle evolution')
    ax.plot(array_name[0], result_all_angle[0], 'yo')
    ax.plot(array_name[save_best_iteration_angle - 1], result_all_angle[save_best_iteration_angle - 1], 'mo')
    ax.plot(array_name[best_iteration - 1], result_all_angle[best_iteration - 1], 'ro')

    ax.plot(array_name, result_all_area, 'bo-', label='area evolution')
    ax.plot(array_name[0], result_all_area[0], 'yo')
    ax.plot(array_name[save_best_iteration_area - 1], result_all_area[save_best_iteration_area - 1], 'mo',
            label='minimum distortion')
    ax.plot(array_name[best_iteration - 1], result_all_area[best_iteration - 1], 'ro',
            label='best iteration')
    ax.legend()

    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    ax.legend()

    print("See the best score general angle "
          + str(result_all_angle[best_iteration - 1]))

    print("See the best score general area "
          + str(result_all_area[best_iteration - 1]))

    return array_complex_number[save_best_iteration_area-1]


def random_complex_abs_value_pourcent(model_sphere_color, plan_complex, model_base, min_random=-100, max_random=100,
                                      nbr_iteration=500):
    """
            random_complex_abs_value_pourcent

            This function create by Laurent DOITEAU.
            Try to find the best parameter to reduce the area distortion.

            :param model_sphere_color: Sphere with texture color
            :type model_sphere_color: Trimesh

            :param plan_complex: This array represent the complex plan.
            :type plan_complex: array[complex_number]

            :param model_base: Base model (Example the Foetus)
            :type model_base: Trimesh

            :param min_random: The minimum for the interval random.
            :type min_random: Integer

            :param max_random: The maximum for the interval random.
            :type max_random: Integer

            :param nbr_iteration: The numbers of iterations to find the best parameters
            :type nbr_iteration: Integer

            :return The best parameter find by this function.

    """
    result_all_angle = []
    result_all_area = []
    array_name = []
    array_complex_number = []

    save_best_iteration_area = 0
    min_area = 1000000000.0

    save_best_iteration_angle = 0
    min_angle = 1000000000.0

    best_iteration = 0
    score = 1000000000.0

    nbrAMin = min_random
    nbrAMax = max_random
    nbrAMin_IMAG = min_random
    nbrAMax_IMAG = max_random

    nbrBMin = min_random
    nbrBMax = max_random
    nbrBMin_IMAG = min_random
    nbrBMax_IMAG = max_random

    nbrCMin = min_random
    nbrCMax = max_random
    nbrCMin_IMAG = min_random
    nbrCMax_IMAG = max_random

    nbrDMin = min_random
    nbrDMax = max_random
    nbrDMin_IMAG = min_random
    nbrDMax_IMAG = max_random

    for i in range(1, nbr_iteration):

        a = complex(uniform(nbrAMin, nbrAMax), uniform(nbrAMin_IMAG, nbrAMax_IMAG))
        b = complex(uniform(nbrBMin, nbrBMax), uniform(nbrBMin_IMAG, nbrBMax_IMAG))
        c = complex(uniform(nbrCMin, nbrCMax), uniform(nbrCMin_IMAG, nbrCMax_IMAG))
        d = complex(uniform(nbrDMin, nbrDMax), uniform(nbrDMin_IMAG, nbrDMax_IMAG))

        array_name.append(i)
        array_complex_number.append([a, b, c, d])

        plan_complex_transfo = mobius_transformation(a, b, c, d, plan_complex)

        real_array = plan_complex_transfo[:].real
        imag_array = plan_complex_transfo[:].imag

        result_plan_complex = []
        for p in range(0, len(real_array)):
            result_plan_complex.append(np.array([real_array[p], imag_array[p], -1]))

        result_plan_complex = np.array(result_plan_complex)

        new_vertices_sphere = sp.inverse_stereo_projection(result_plan_complex)
        model_transform_sphere = trimesh.Trimesh(vertices=new_vertices_sphere,
                                                 faces=model_sphere_color.faces,
                                                 vertex_colors=model_sphere_color.visual.vertex_colors,
                                                 process=False)

        result_angle = abs((model_transform_sphere.face_angles / np.sum(model_transform_sphere.face_angles))
                           - (model_base.face_angles / np.sum(model_base.face_angles)))
        result_angle_pourcent = np.sum(result_angle) * 100
        result_all_angle.append(result_angle_pourcent)

        result_area = abs((model_transform_sphere.area_faces / np.sum(model_transform_sphere.area_faces))
                          - (model_base.area_faces / np.sum(model_base.area_faces)))
        result_area_pourcent = np.sum(result_area) * 100

        result_all_area.append(result_area_pourcent)

        if min_angle > result_angle_pourcent:
            min_angle = result_angle_pourcent
            save_best_iteration_angle = i

        if min_area > result_area_pourcent:
            save_best_iteration_area = i
            min_area = result_area_pourcent

        if score > result_area_pourcent + result_angle_pourcent:
            score = result_area_pourcent + result_angle_pourcent
            best_iteration = i
            if a.real >= 0:
                nbrAMax = a.real
            else:
                nbrAMin = a.real
            if a.imag >= 0:
                nbrAMax_IMAG = a.imag
            else:
                nbrAMin_IMAG = a.imag

            if b.real >= 0:
                nbrBMax = b.real
            else:
                nbrBMin = b.real
            if b.imag >= 0:
                nbrBMax_IMAG = b.imag
            else:
                nbrBMin_IMAG = b.imag

            if c.real >= 0:
                nbrCMax = c.real
            else:
                nbrCMin = c.real
            if c.imag >= 0:
                nbrCMax_IMAG = c.imag
            else:
                nbrCMin_IMAG = c.imag

            if d.real >= 0:
                nbrDMax = d.real
            else:
                nbrDMin = d.real
            if d.imag >= 0:
                nbrDMax_IMAG = d.imag
            else:
                nbrDMin_IMAG = d.imag

    fig, ax = plt.subplots(1, 1)
    ax.set_title('Distortion evolution mediane')
    ax.set_xlabel('Number of tests')
    ax.set_ylabel('Distortion mm² (mediane)')

    ax.plot(array_name, result_all_angle, 'go-', label='angle evolution')
    ax.plot(array_name[0], result_all_angle[0], 'yo')
    ax.plot(array_name[save_best_iteration_angle - 1], result_all_angle[save_best_iteration_angle - 1], 'mo')
    ax.plot(array_name[best_iteration - 1], result_all_angle[best_iteration - 1], 'ro')

    ax.plot(array_name, result_all_area, 'bo-', label='area evolution')
    ax.plot(array_name[0], result_all_area[0], 'yo')
    ax.plot(array_name[save_best_iteration_area - 1], result_all_area[save_best_iteration_area - 1], 'mo',
            label='minimum distortion')
    ax.plot(array_name[best_iteration - 1], result_all_area[best_iteration - 1], 'ro',
            label='best iteration')
    ax.legend()

    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    ax.legend()

    print("See the best score general angle "
          + str(result_all_angle[best_iteration - 1]))

    print("See the best score general area "
          + str(result_all_area[best_iteration - 1]))

    return array_complex_number[save_best_iteration_area-1]

"""
=============================================================================
======================= Func mobius_angle_complex_a # (obsolete) ========================
=============================================================================
"""


def mobius_angle_complex_a(model_sphere_color, plan_complex, model_base,
                           b=complex(0., 0.),
                           c=complex(0., 0.),
                           d=complex(1., 0.)):
    """
            mobius_angle_complex_a

            This function try all variant for parameter a with his angle.

            :param model_sphere_color: Sphere with texture color
            :type model_sphere_color: Trimesh

            :param plan_complex: This array represent the complex plan.
            :type plan_complex: array[complex_number]

            :param model_base: Base model (Example the Foetus)
            :type model_base: Trimesh

            :param b: Complex number or Integer (parameter to transform the plan)
            :type b: Complex or Integer

            :param c: Complex number or Integer (parameter to transform the plan)
            :type c: Complex or Integer

            :param d: Complex number or Integer (parameter to transform the plan)
            :type d: Complex or Integer

            :return The best parameter find by this function.

    """
    result_all_angle = []
    result_all_area = []
    array_name = []
    best_complex = []

    save_best_iteration_angle = 0
    min_angle = 1000000000.0

    save_best_iteration_area = 0
    min_area = 1000000000.0

    for i in range(0, 360):

        array_name.append(i+1)
        a = complex(math.cos(i), math.sin(360 - i))

        plan_complex_transfo = mobius_transformation(a, b, c, d, plan_complex)

        real_array = plan_complex_transfo[:].real
        imag_array = plan_complex_transfo[:].imag

        result_plan_complex = []
        for p in range(0, len(real_array)):
            result_plan_complex.append(np.array([real_array[p], imag_array[p], -1]))

        result_plan_complex = np.array(result_plan_complex)

        new_vertices_sphere = sp.inverse_stereo_projection(result_plan_complex)
        model_transform_sphere = trimesh.Trimesh(vertices=new_vertices_sphere,
                                                 faces=model_sphere_color.faces,
                                                 vertex_colors=model_sphere_color.visual.vertex_colors,
                                                 process=False)

        result_angle = abs((model_transform_sphere.face_angles / np.sum(model_transform_sphere.face_angles))
                           - (model_base.face_angles / np.sum(model_base.face_angles)))
        result_angle_pourcent = np.sum(result_angle) * 100
        result_all_angle.append(result_angle_pourcent)

        result_area = abs((model_transform_sphere.area_faces / np.sum(model_transform_sphere.area_faces))
                          - (model_base.area_faces / np.sum(model_base.area_faces)))
        result_area_pourcent = np.sum(result_area) * 100
        result_all_area.append(result_area_pourcent)

        if min_angle > result_angle_pourcent:
            min_angle = result_angle_pourcent
            save_best_iteration_angle = i

        if min_area > result_area_pourcent:
            min_area = result_area_pourcent
            save_best_iteration_area = i
            best_complex = [a, b, c, d]

    fig, ax = plt.subplots(1, 1)
    plt.bar(array_name, result_all_angle)
    ax.set_title('Distorsion angle evolution (of complex a)')
    ax.set_xlabel('Number of tests')
    ax.set_ylabel('% distorsion angle')
    ax.plot(array_name, result_all_angle, 'r-')

    fig, ax = plt.subplots(1, 1)
    plt.bar(array_name, result_all_area)
    ax.set_title('Distorsion area evolution (of complex a)')
    ax.set_xlabel('Number of tests')
    ax.set_ylabel('% distorsion area')
    ax.plot(array_name, result_all_area, 'r-')

    fig, ax = plt.subplots(1, 1)
    ax.set_title('Distorsion evolution')
    ax.set_xlabel('Number of tests')
    ax.set_ylabel('% distorsion')

    ax.plot(array_name, result_all_angle, 'go-', label='angle evolution')
    ax.plot(array_name[0], result_all_angle[0], 'yo')
    ax.plot(array_name[save_best_iteration_angle], result_all_angle[save_best_iteration_angle], 'ro')

    ax.plot(array_name, result_all_area, 'bo-', label='area evolution')
    ax.plot(array_name[0], result_all_area[0], 'yo')
    ax.plot(array_name[save_best_iteration_area], result_all_area[save_best_iteration_area], 'ro',
            label='minimum distortion')
    ax.legend()

    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')

    print("See the best score for angle with "
          + str(min_angle) + "%")

    print("See the best score for area with "
          + str(min_area) + "%")

    return best_complex