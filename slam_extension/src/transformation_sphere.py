import numpy as np
from random import *
import matplotlib.pyplot as plt
import trimesh
import math
from scipy.optimize import minimize

import src.stereo_projection as sp


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
    if (c*array_complex) + d != 0:
        numerator = (a * array_complex) + b
        denominator = (c * array_complex) + d

        result = numerator / denominator

    return result


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
                                             vertex_colors=model_sphere_color.visual.vertex_colors)

    result_angle = abs((model_transform_sphere.face_angles / np.sum(model_transform_sphere.face_angles))
                       - (model_base.face_angles / np.sum(model_base.face_angles)))
    result_angle_pourcent = np.sum(result_angle) * 100

    if array_angle_result is not None:
        array_angle_result.append(result_angle_pourcent)

    result_area = abs((model_transform_sphere.area_faces / np.sum(model_transform_sphere.area_faces))
                      - (model_base.area_faces / np.sum(model_base.area_faces)))

                   # / (model_base.area_faces / np.sum(model_base.area_faces))) * 100

    # result_area = np.sort(result_area, axis=None)
    result_area_pourcent = np.sum(result_area) * 100
    # result_area_pourcent_median = result_area[int(len(result_area)/2)]
    # result_area_pourcent_moy = np.sum(result_area)/len(result_area)

    if array_area_result is not None:
        array_area_result.append(result_area_pourcent)

    # print("median : " + str(result_area_pourcent_median))
    # print("moy : " + str(result_area_pourcent_moy))

    return result_area_pourcent


def random_complex(model_sphere_color, plan_complex, model_base, min_random=-100, max_random=100, nbr_iteration=500):
    """
            random_complex

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
                                                 vertex_colors=model_sphere_color.visual.vertex_colors)

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
    ax.set_title('Distorsion angle evolution')
    ax.set_xlabel('Number of tests')
    ax.set_ylabel('% distorsion angle')

    fig, ax = plt.subplots(1, 1)
    plt.bar(array_name, result_all_area)
    ax.set_title('Distorsion area evolution')
    ax.set_xlabel('Number of tests')
    ax.set_ylabel('% distorsion area')

    print("See the best score for area (" + str(save_best_iteration_area) + " iteration) with "
          + str(result_all_area[save_best_iteration_area-1]) + "%")

    print("See the best score for angle (" + str(save_best_iteration_angle) + " iteration) with "
          + str(result_all_angle[save_best_iteration_angle-1]) + "%")

    return array_complex_number[save_best_iteration_area-1]


def random_complex_with_minimize(model_sphere_color, plan_complex, model_base, min_random=-100, max_random=100, nbr_iteration=10):
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
    result_all_area = []
    array_name = []
    array_result = []

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
                                                 vertex_colors=model_sphere_color.visual.vertex_colors)

        result_area = abs((model_transform_sphere.area_faces / np.sum(model_transform_sphere.area_faces))
                          - (model_base.area_faces / np.sum(model_base.area_faces)))

        result_area_pourcent = np.sum(result_area) * 100

        result_all_area.append(result_area_pourcent)

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
    plt.bar(array_name, result_all_area)
    ax.set_title('Distorsion area evolution')
    ax.set_xlabel('Number of tests')
    ax.set_ylabel('% distorsion area')

    print("See the best score for area (" + str(save_best_iteration_area) + " iteration) with "
          + str(result_all_area[save_best_iteration_area - 1]) + "%")

    return array_result[save_best_iteration_area - 1]


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

    min_array = 10000000000000000000000

    for i in range(0, 360):

        array_name.append(i)
        a = complex(math.cos(i), math.sin(i))

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
                                                 vertex_colors=model_sphere_color.visual.vertex_colors)

        result_angle = abs((model_transform_sphere.face_angles / np.sum(model_transform_sphere.face_angles))
                           - (model_base.face_angles / np.sum(model_base.face_angles)))
        result_angle_pourcent = np.sum(result_angle) * 100
        result_all_angle.append(result_angle_pourcent)

        result_area = abs((model_transform_sphere.area_faces / np.sum(model_transform_sphere.area_faces))
                          - (model_base.area_faces / np.sum(model_base.area_faces)))
        result_area_pourcent = np.sum(result_area) * 100
        result_all_area.append(result_area_pourcent)

        if min_array > result_area_pourcent:
            min_array = result_area_pourcent
            best_complex = [a, b, c, d]

    fig, ax = plt.subplots(1, 1)
    plt.bar(array_name, result_all_angle)
    ax.set_title('Distorsion angle evolution (of complex a)')
    ax.set_xlabel('Number of tests')
    ax.set_ylabel('% distorsion angle')

    fig, ax = plt.subplots(1, 1)
    plt.bar(array_name, result_all_area)
    ax.set_title('Distorsion area evolution (of complex a)')
    ax.set_xlabel('Number of tests')
    ax.set_ylabel('% distorsion area')

    return best_complex
