from .base import CipherAlgorithm

class CaesarCipher(CipherAlgorithm):
    name = "Caesar Cipher"
    category = "Classical"
    requires_key = True
    key_type = "Numeric Shift"
    security_level = "Educational / Historical"
    description = "Shifts each ASCII English letter by a fixed number of positions."
    working = [
        "Convert the shift value to an integer.",
        "For each ASCII letter, move forward through A–Z or a–z.",
        "Wrap around the alphabet using modulo 26.",
        "Decryption applies the same process with the negative shift."
    ]
    example = {"input": "HELLO", "key": "3", "output": "KHOOR"}

    @staticmethod
    def _is_ascii_letter(char):
        return ("A" <= char <= "Z") or ("a" <= char <= "z")

    def _shift(self, text, shift):
        result = []
        for char in text:
            if self._is_ascii_letter(char):
                start = ord("A") if "A" <= char <= "Z" else ord("a")
                result.append(chr((ord(char) - start + shift) % 26 + start))
            else:
                result.append(char)
        return "".join(result)

    @staticmethod
    def _parse_key(key):
        try:
            return int(key)
        except (ValueError, TypeError):
            raise ValueError("Shift value must be a valid integer.")

    def encrypt(self, text, key=None):
        return self._shift(text, self._parse_key(key))

    def decrypt(self, text, key=None):
        return self._shift(text, -self._parse_key(key))
