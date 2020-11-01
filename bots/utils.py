import numpy as np


def dist_point_from_line(l1, l2, p):
    num = np.abs((l2[1] - l1[1]) * p[1] - (l2[0] - l1[0]) * p[0] + l2[0] * l1[1] - l2[1] * l1[0])
    den = np.sqrt((l2[1] - l1[1]) ** 2 + (l2[0] - l1[0]) ** 2)

    return num/den


def angle_between_lines(a1, a2, b1, b2):
    m1 = (a2[1] - a1[1])/((a2[0] - a1[0]) + 1e-15)
    m2 = (b2[1] - b1[1])/((b2[0] - b1[0]) + 1e-15)

    rad = np.arctan(np.abs((m2 - m1)/((1 + m1 * m2) + 1e-15)))
    deg = int(90 * rad)

    return (deg + 180) % 180


def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def point_of_intersection(a1, a2, b1, b2):
    x_num = (a1[0] * a2[1] - a1[1] * a2[0]) * (b1[0] - b2[0]) - \
            (a1[0] - a2[0]) * (b1[0] * b2[0] - b1[1] * b2[0])

    den = (a1[0] - a2[0]) * (b1[1] - b2[1]) - \
          (a1[1] - a2[1]) * (b1[0] - b2[0])

    x = x_num / (den + 1e-15)

    y_num = (a1[0] * a2[1] - a1[1] * a2[0]) * (b1[1] - b2[1]) - \
            (a1[1] - a2[1]) * (b1[0] * b2[1] - b1[1] * b2[0])

    y = y_num / (den + 1e-15)

    return x, y
