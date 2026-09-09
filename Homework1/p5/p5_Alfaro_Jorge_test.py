"""Unit tests for the Caesar cipher and letter frequency functions."""

import unittest
from p5_Alfaro_Jorge import caesar_cipher, caesar_decipher, letter_frequency


class CaesarCipherTests(unittest.TestCase):
    def test_known_cipher_and_wraparound(self):
        self.assertEqual(caesar_cipher("Hello, Zebra!", 3), "Khoor, Cheud!")

    def test_known_decipher(self):
        self.assertEqual(caesar_decipher("Khoor, Cheud!", 3), "Hello, Zebra!")

    def test_negative_and_large_shifts(self):
        self.assertEqual(caesar_cipher("Abc XYZ", -1), "Zab WXY")
        self.assertEqual(caesar_cipher("Abc XYZ", 27), "Bcd YZA")

    def test_empty_and_nonletters(self):
        self.assertEqual(caesar_cipher("", 3), "")
        self.assertEqual(caesar_cipher("123 !?\n", 8), "123 !?\n")

    def test_round_trip(self):
        for shift in (-53, -1, 0, 26, 57):
            text = "Mixed CASE, spaces and 123!"
            self.assertEqual(caesar_decipher(caesar_cipher(text, shift), shift), text)

    def test_frequency_ignores_case_and_nonletters(self):
        expected = {letter: 0 for letter in "abcdefghijklmnopqrstuvwxyz"}
        expected.update({"a": 3, "b": 2, "z": 1})
        self.assertEqual(letter_frequency("AaA bB! Z 123"), expected)

    def test_empty_frequency(self):
        self.assertEqual(letter_frequency(""), dict.fromkeys("abcdefghijklmnopqrstuvwxyz", 0))


if __name__ == "__main__":
    unittest.main()
