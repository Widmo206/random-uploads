# -*- coding: utf-8 -*-
"""Integrale de Riemann

Created on 2025-08.21

@author: jakub.mnn
"""


from typing import Callable
import scipy.integrate as spintegrate
import matplotlib.pyplot as plt
import numpy as np


formats = iter(["r-", "y-", "g-", "c-", "b-", "m-"])


def main():
    # function 1
    print("Function 1: f(x) = (1 - x**2) ** 0.5")
    print("Lower bound:")
    a = get_input(float, prompt="a = ")
    print("Upper bound:")
    b = get_input(float, prompt="b = ")
    print("No. sub-intervals:")
    N = get_input(int, True, (0, 10000), prompt="N = ")

    plot(f1, a, b, N, title="Graph of $f(x)=\sqrt{1-x^{2}}$")

    print(f"Rieman sum (left):  {riemann_left(f1, a, b, N)}")
    print(f"Rieman sum (right): {riemann_right(f1, a, b, N)}")
    result, error = spintegrate.quad(f1, a, b)
    print(f"Integral (scipy):   {result}\n    -> error: {error}")


    print()


    # function 2
    print("Function 2: f(x) = 1 / (2 * np.pi)**2 * np.e**(-x**2 / 2)")
    print("Lower bound:")
    a = get_input(float, prompt="a = ")
    print("Upper bound:")
    b = get_input(float, prompt="b = ")
    print("No. sub-intervals:")
    N = get_input(int, True, (0, 10000), prompt="N = ")

    plot(f2, a, b, N, title="Graph of $\Phi(x)=\frac{1}{\sqrt{2 \pi}} e^{-x^{2}/2}$")

    print(f"Rieman sum (left):  {riemann_left(f2, a, b, N)}")
    print(f"Rieman sum (right): {riemann_right(f2, a, b, N)}")
    result, error = spintegrate.quad(f2, a, b)
    print(f"Integral (scipy):   {result}\n    -> error: {error}")



def f1(x: float) -> float:
    return (1 - x**2) ** 0.5

def f2(x: float) -> float:
    return 1 / (2 * np.pi)**2 * np.e**(-x**2 / 2)


def riemann_left(f: Callable, a: float, b: float, N: int) -> float:
    dx = (b - a) / N

    _sum = 0.0

    for i in range(N):
        x = a + i * dx

        _sum += f(x) * dx

    return _sum


def riemann_right(f: Callable, a: float, b: float, N: int) -> float:
    dx = (b - a) / N

    _sum = 0.0

    for i in range(1, N+1):
        x = a + i * dx

        _sum += f(x) * dx

    return _sum


def plot(func: Callable, a: float, b: float, points: int=101, title: str=None):
    zero = np.linspace(0, 0, points)
    interval = np.linspace(a, b, points)

    if title is None:
        title = f"Graph of {func.__name__}(x)"
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend(loc="upper right")
    plt.grid(True)

    plt.plot(interval, zero, "k--", label="x = 0")
    plt.plot(interval, func(interval), next(formats), label=f"{func.__name__}(x)")

    plt.show()


def get_input(desired_type: type=str, check_bounds=False,
              bounds: tuple[float | int | None]=(None, None),
              prompt: str="> ") -> ...:
    """Get input from the user, cast it to the correct type and check that it's
    within bounds.

    No bounds by default.
    """
    # In use since 2025.01.15 :)
    while True:
        raw_in = input(prompt)

        try:
            typed_in = desired_type(raw_in)
        except ValueError:
            continue

        # check bounds
        if bounds != (None, None):
            if desired_type == int or desired_type == float:
                value = typed_in
            else:
                try:
                    value = len(typed_in)
                except:
                    raise TypeError(f"Cannot check bounds of an instance of {desired_type}")
                    value = None

            # Lower bound
            if bounds[0] is not None:
                if value < bounds[0]:
                    # discard out-of-bounds value
                    continue

            # Upper bound
            if bounds[1] is not None:
                if value > bounds[1]:
                    # discard out-of-bounds value
                    continue

        return typed_in


if __name__ == "__main__":
    main()
