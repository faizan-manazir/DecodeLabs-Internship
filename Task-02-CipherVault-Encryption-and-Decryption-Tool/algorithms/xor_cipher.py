from .base import CipherAlgorithm
import base64, binascii

class XORCipher(CipherAlgorithm):
    name = "XOR Cipher"
    category = "Key-Based"
    requires_key = True
    key_type = "Secret Key"
    security_level = "Educational / Key-Based Transformation"
    description = "XORs UTF-8 bytes with a repeating secret key and Base64-encodes the result."
    working = [
        "Convert the text and secret key to UTF-8 bytes.",
        "Repeat the key until it covers the message.",
        "XOR each message byte with the corresponding key byte.",
        "Base64-encode ciphertext so it can be safely displayed and copied.",
        "Applying XOR again with the same key reverses the transformation."
    ]
    example = {"input": "HELLO", "key": "KEY", "output": "Base64 encoded output"}

    @staticmethod
    def _key_bytes(key):
        if not isinstance(key, str) or not key:
            raise ValueError("Secret key is required.")
        data = key.encode("utf-8")
        if not data:
            raise ValueError("Secret key is required.")
        return data

    @staticmethod
    def _xor(data, key):
        return bytes(byte ^ key[i % len(key)] for i, byte in enumerate(data))

    def encrypt(self, text, key=None):
        result = self._xor(text.encode("utf-8"), self._key_bytes(key))
        return base64.b64encode(result).decode("ascii")

    def decrypt(self, text, key=None):
        try:
            data = base64.b64decode(text.encode("ascii"), validate=True)
        except (ValueError, UnicodeEncodeError, binascii.Error):
            raise ValueError("Ciphertext is not valid Base64.")
        try:
            return self._xor(data, self._key_bytes(key)).decode("utf-8")
        except UnicodeDecodeError:
            raise ValueError("Decryption failed. Check the secret key and ciphertext.")
