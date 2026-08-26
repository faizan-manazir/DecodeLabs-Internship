from .base import CipherAlgorithm

class VigenereCipher(CipherAlgorithm):
    name = "Vigenère Cipher"
    category = "Classical"
    requires_key = True
    key_type = "Keyword"
    security_level = "Educational / Historical"
    description = "A keyword-based polyalphabetic substitution cipher."
    working = [
        "Keep ASCII English letters from the keyword and reject an empty usable key.",
        "Repeat the keyword across alphabetic characters in the message.",
        "Convert each key letter to a shift from 0 to 25.",
        "Encrypt by adding the shift; decrypt by subtracting it."
    ]
    example = {"input": "HELLO", "key": "KEY", "output": "RIJVS"}

    @staticmethod
    def _key_shifts(key):
        if not isinstance(key, str):
            raise ValueError("Keyword must be text.")
        letters = [ord(c.lower()) - ord("a") for c in key if ("A" <= c <= "Z") or ("a" <= c <= "z")]
        if not letters:
            raise ValueError("Keyword must contain at least one ASCII English letter.")
        return letters

    def _process(self, text, key, decrypt=False):
        shifts = self._key_shifts(key)
        result, index = [], 0
        for char in text:
            if ("A" <= char <= "Z") or ("a" <= char <= "z"):
                start = ord("A") if char.isupper() else ord("a")
                shift = shifts[index % len(shifts)]
                if decrypt:
                    shift = -shift
                result.append(chr((ord(char) - start + shift) % 26 + start))
                index += 1
            else:
                result.append(char)
        return "".join(result)

    def encrypt(self, text, key=None):
        return self._process(text, key, False)

    def decrypt(self, text, key=None):
        return self._process(text, key, True)
