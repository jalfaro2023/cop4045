"""Find all ordered Pythagorean triples with sides at most n."""


def find_Pythagorean(n):
    """Return triples by trying every positive side combination."""
    triples = []
    for a in range(1, n + 1):
        for b in range(1, n + 1):
            for c in range(1, n + 1):
                if a ** 2 + b ** 2 == c ** 2:
                    triples.append((a, b, c))
    return triples


if __name__ == "__main__":
    n = int(input("Enter a positive integer n: "))
    for triple in find_Pythagorean(n):
        print(triple)
