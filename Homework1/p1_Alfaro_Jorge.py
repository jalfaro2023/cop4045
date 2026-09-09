"""Solve and plot quadratic equations using 150 sample points."""

import math
import matplotlib.pyplot as plt


def main():
    """Read coefficients until the user leaves a blank."""
    while True:
        a_text = input("Enter a (ENTER to quit): ")
        if a_text == "":
            break
        a = float(a_text)
        b = float(input("Enter b: "))
        c = float(input("Enter c: "))
        discriminant = b ** 2 - 4 * a * c
        center = -b / (2 * a)
        half_width = 3.0
        if discriminant < 0:
            print("no real solutions")
        elif discriminant == 0:
            print("one solution: {:.5f}".format(center))
        else:
            x1 = (-b - math.sqrt(discriminant)) / (2 * a)
            x2 = (-b + math.sqrt(discriminant)) / (2 * a)
            print("two solutions: x1={:.5f} x2={:.5f}".format(x1, x2))
            half_width = max(3.0, abs(x2 - x1) / 2 + 2)

        xmin = center - half_width
        xmax = center + half_width
        xs = [xmin + (xmax - xmin) * i / 149 for i in range(150)]
        ys = [a * x ** 2 + b * x + c for x in xs]
        plt.figure()
        plt.plot(xs, ys)
        plt.axhline(0, color="gray", linewidth=0.8)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("y = {}x^2 + {}x + {}".format(a, b, c))
        plt.grid(True)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    main()
