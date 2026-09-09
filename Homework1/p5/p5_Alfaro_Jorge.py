"""Encrypt, decrypt, and count English letters in terminal messages."""

LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def caesar_cipher(text, shift):
    """Shift English letters, preserving case and all other characters."""
    result = ""
    for character in text:
        if character in LOWERCASE:
            alphabet = LOWERCASE
        elif character in UPPERCASE:
            alphabet = UPPERCASE
        else:
            result += character
            continue
        for index in range(len(alphabet)):
            if character == alphabet[index]:
                result += alphabet[(index + shift) % 26]
                break
    return result


def caesar_decipher(cyphertext, shift):
    """Undo a Caesar shift and return the original text."""
    return caesar_cipher(cyphertext, -shift)


def letter_frequency(text):
    """Return counts for all 26 English letters, ignoring case."""
    counts = {letter: 0 for letter in LOWERCASE}
    for character in text.lower():
        if character in counts:
            counts[character] += 1
    return counts


def main():
    """Offer repeated message encryption and analysis until quit."""
    while True:
        print("\n1. Encrypt and analyze a message\n2. Quit")
        choice = input("Choose an option: ")
        if choice == "2":
            break
        if choice != "1":
            print("Please choose 1 or 2.")
            continue
        text = input("Enter a message: ")
        try:
            shift = int(input("Enter an integer shift: "))
        except ValueError:
            print("The shift must be an integer.")
            continue
        ciphered = caesar_cipher(text, shift)
        print("Ciphered text:", ciphered)
        print("Letter frequencies in the original message:")
        for letter, count in letter_frequency(text).items():
            print("{}: {}".format(letter, count))
        print("Deciphered text:", caesar_decipher(ciphered, shift))


if __name__ == "__main__":
    main()
