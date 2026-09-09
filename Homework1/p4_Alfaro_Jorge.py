"""Tabulate and plot a user-supplied mathematical expression."""

import math
import matplotlib.pyplot as plt


def plot_function(fun_str, domain, ns):
    """Print and plot ns equally spaced samples, including both endpoints."""
    if ns < 2:
        raise ValueError("At least two samples are required.")
    xmin, xmax = domain
    xs = [xmin + (xmax - xmin) * i / (ns - 1) for i in range(ns)]
    ys = []
    for x in xs:
        y = eval(fun_str)
        ys.append(y)

    print("{:>12} {:>12}".format("x", "y"))
    for x, y in zip(xs, ys):
        print("{:+12.4f} {:+12.4f}".format(x, y))
    plt.figure()
    plt.plot(xs, ys)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(fun_str)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    fun_str = input("Enter function with variable x: ")
    ns = int(input("Enter number of samples: "))
    xmin = float(input("Enter xmin: "))
    xmax = float(input("Enter xmax: "))
    plot_function(fun_str, (xmin, xmax), ns)
