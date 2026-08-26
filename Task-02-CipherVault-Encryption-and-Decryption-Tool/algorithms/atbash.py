from .base import CipherAlgorithm

class AtbashCipher(CipherAlgorithm):
    name = "Atbash Cipher"
    category = "Classical"
    requires_key = False
    key_type = "None"
    security_level = "Educational / Historical"
    description = "A fixed substitution cipher that mirrors ASCII English letters across the alphabet."
    working = [
        "Map A to Z, B to Y, C to X, and so on.",
        "Preserve case, spaces, punctuation, numbers, and non-ASCII characters.",
        "The same transformation is used for encryption and decryption."
    ]
    example = {"input": "HELLO", "key": "None", "output": "SVOOL"}

    def _process(self, text):
        result = []
        for char in text:
            if "A" <= char <= "Z":
                result.append(chr(ord("Z") - (ord(char) - ord("A"))))
            elif "a" <= char <= "z":
                result.append(chr(ord("z") - (ord(char) - ord("a"))))
            else:
                result.append(char)
        return "".join(result)

    def encrypt(self, text, key=None): return self._process(text)
    def decrypt(self, text, key=None): return self._process(text)
