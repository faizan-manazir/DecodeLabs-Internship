from .base import CipherAlgorithm

class RailFenceCipher(CipherAlgorithm):
    name = "Rail Fence Cipher"
    category = "Classical"
    requires_key = True
    key_type = "Numeric Rails"
    security_level = "Educational / Historical"
    description = "A transposition cipher that writes text in a zig-zag pattern across multiple rails."
    working = [
        "Choose the number of rails.",
        "Write characters diagonally down and up across the rails.",
        "Read each rail from top to bottom to form ciphertext.",
        "Decryption reconstructs the zig-zag positions before reading the original order."
    ]
    example = {"input": "WEAREDISCOVEREDFLEEATONCE", "key": "3", "output": "WECRLTEERDSOEEFEAOCAIVDEN"}

    @staticmethod
    def _rails(key):
        try:
            rails = int(key)
        except (TypeError, ValueError):
            raise ValueError("Number of rails must be a valid integer >= 2.")
        if rails < 2:
            raise ValueError("Number of rails must be at least 2.")
        return rails

    @staticmethod
    def _pattern(length, rails):
        row, direction, pattern = 0, 1, []
        for _ in range(length):
            pattern.append(row)
            if row == 0:
                direction = 1
            elif row == rails - 1:
                direction = -1
            row += direction
        return pattern

    def encrypt(self, text, key=None):
        if not text: return ""
        rails = self._rails(key)
        if rails >= len(text): return text
        buckets = [""] * rails
        for char, row in zip(text, self._pattern(len(text), rails)):
            buckets[row] += char
        return "".join(buckets)

    def decrypt(self, text, key=None):
        if not text: return ""
        rails = self._rails(key)
        if rails >= len(text): return text
        pattern = self._pattern(len(text), rails)
        counts = [pattern.count(row) for row in range(rails)]
        rows, index = [], 0
        for count in counts:
            rows.append(list(text[index:index+count]))
            index += count
        positions = [0] * rails
        result = []
        for row in pattern:
            result.append(rows[row][positions[row]])
            positions[row] += 1
        return "".join(result)
