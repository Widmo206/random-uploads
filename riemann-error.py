# -*- coding: utf-8 -*-
"""Erreur de l'integrale de Riemann en fonction de N

Created on 2025-08.21

@author: jakub.mnn
"""


from typing import Callable
import scipy.integrate as spintegrate
from scipy.differentiate import derivative
import matplotlib.pyplot as plt
import numpy as np


formats = iter(["r-", "y-", "g-", "c-", "b-", "m-"])


def main():
    a, b = 0, 10

    max_n = 1000


    zero = np.linspace(0, 0, max_n)
    N = np.linspace(1, max_n, max_n)


    plt.title("Graph of error as a function of N")
    plt.xlabel("N")
    plt.ylabel("error")
    plt.grid(True)
    plt.semilogy()

    # plt.plot(N, zero, "k--", label="x = 0")
    plt.plot(N, expected_error(f, a, b, N), next(formats), label="expected error")

    integral = spintegrate.quad(f, a, b)

    plt.plot(N, [integral - riemann_left(f, a, b, n) for n in N], next(formats), label="Error of Rieman sum (left)")
    plt.plot(N, [integral - riemann_right(f, a, b, n) for n in N], next(formats), label="Error of Rieman sum (right)")

    plt.legend(loc="upper right")
    plt.show()





def f(x: float) -> float:
    return 2*x + 3


def expected_error(f: Callable, a: float, b: float, N: int) -> float:
    x = np.linspace(a, b, 1000)
    return (b - a)**2 / (2*N) * float(max(derivative(f, x).df))


def riemann_left(f: Callable, a: float, b: float, N: int) -> float:
    dx = (b - a) / N

    _sum = 0.0

    for i in range(int(N)):
        x = a + i * dx

        _sum += f(x) * dx

    return _sum


def riemann_right(f: Callable, a: float, b: float, N: int) -> float:
    dx = (b - a) / N

    _sum = 0.0

    for i in range(int(N)):
        x = a + i * dx

        _sum += f(x) * dx

    return _sum


if __name__ == "__main__":
    main()
