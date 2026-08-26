from .base import CipherAlgorithm
import base64, os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.exceptions import InvalidTag

class AESGCMCipher(CipherAlgorithm):
    name = "AES-256-GCM"
    category = "Modern"
    requires_key = True
    key_type = "Password"
    security_level = "Modern Authenticated Encryption"
    description = "AES-256-GCM provides confidentiality and tamper detection using a password-derived key."
    working = [
        "Generate a fresh random 16-byte salt and 12-byte GCM nonce.",
        "Use scrypt to derive a 256-bit AES key from the password and salt.",
        "Encrypt and authenticate the UTF-8 message with AES-GCM.",
        "Package a version marker, salt, nonce, and ciphertext into Base64.",
        "Decryption derives the same key and verifies the authentication tag."
    ]
    example = {"input": "Hello", "key": "Strong password", "output": "Randomized authenticated ciphertext"}

    @staticmethod
    def _derive_key(password, salt):
        if not isinstance(password, str) or not password:
            raise ValueError("Password is required.")
        kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
        return kdf.derive(password.encode("utf-8"))

    def encrypt(self, text, key=None):
        salt, nonce = os.urandom(16), os.urandom(12)
        ciphertext = AESGCM(self._derive_key(key, salt)).encrypt(nonce, text.encode("utf-8"), b"CipherVault:v1")
        return base64.urlsafe_b64encode(b"CVA1" + salt + nonce + ciphertext).decode("ascii")

    def decrypt(self, text, key=None):
        try:
            package = base64.urlsafe_b64decode(text.encode("ascii"))
            if not package.startswith(b"CVA1") or len(package) < 4 + 16 + 12 + 16:
                raise ValueError
            salt, nonce, ciphertext = package[4:20], package[20:32], package[32:]
            plain = AESGCM(self._derive_key(key, salt)).decrypt(nonce, ciphertext, b"CipherVault:v1")
            return plain.decode("utf-8")
        except (ValueError, InvalidTag, UnicodeEncodeError, UnicodeDecodeError):
            raise ValueError("Decryption failed. Check the password and encrypted data.")
