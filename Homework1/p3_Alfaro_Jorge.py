"""Find duplicated substrings without overlapping occurrences."""


def find_dup_str(s, n):
    """Return the earliest substring of length n repeated without overlap."""
    if n <= 0:
        return ""
    for start in range(len(s) - 2 * n + 1):
        candidate = s[start:start + n]
        for second in range(start + n, len(s) - n + 1):
            if candidate == s[second:second + n]:
                return candidate
    return ""


def find_max_dup(s):
    """Return the longest non-overlapping duplicate, earliest on ties."""
    for n in range(len(s) // 2, 0, -1):
        duplicate = find_dup_str(s, n)
        if duplicate:
            return duplicate
    return ""


if __name__ == "__main__":
    s = input("Enter a string: ")
    n = int(input("Enter substring length: "))
    print(find_dup_str(s, n))
    s = input("Enter a string for the longest duplicate: ")
    print(find_max_dup(s))
