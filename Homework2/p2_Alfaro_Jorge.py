"""Problem 2: list and dictionary comprehensions."""


def main() -> None:
    """Display the answers for parts a through f."""
    print("Student: Jorge Alfaro | FAU ID: Z23697022 | Problem 2")

    # a. Include every ordered tuple of four distinct integers.
    equal_squares = [
        (a, b, c, d)
        for a in range(1, 11) for b in range(1, 11)
        for c in range(1, 11) for d in range(1, 11)
        if len({a, b, c, d}) == 4 and a * a + b * b == c * c + d * d
    ]
    print("a:", equal_squares)

    # b. Lowercase words whose original length is less than five.
    words = ['One', 'SEVEN', 'three', 'two', 'Ten']
    short_words = [(word.lower(), len(word)) for word in words if len(word) < 5]
    print("b:", short_words)

    # c. Abbreviate the middle name in each three-part name.
    names = ['Christopher Ashton Kutcher', 'Elizabeth Stamatina Fey']
    abbreviated = [
        f"{first} {middle[0]}. {last}"
        for name in names for first, middle, last in [name.split()]
    ]
    print("c:", abbreviated)

    # d. Compare sorted lowercase characters to identify anagrams.
    lst1 = ["Spam", "Trams", "Elbows", "Tops", "Astral"]
    lst2 = ["Bowels", "Sample", "Altars", "Stop", "Course", "Smart"]
    anagrams = [(w1, w2) for w1 in lst1 for w2 in lst2
                if sorted(w1.lower()) == sorted(w2.lower())]
    print("d:", anagrams)

    # e. Map each distinct string to its length.
    s = ['one', 'two', 'three']
    lengths = {word: len(word) for word in s}
    print("e:", lengths)

    # f. Retain vowel positions and their original character case.
    text = "Hello world"
    vowels = {i: c for i, c in enumerate(text) if c.lower() in "aeiou"}
    print("f:", vowels)


if __name__ == "__main__":
    main()
