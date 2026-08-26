from .base import CipherAlgorithm
import base64, os
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

class FernetCipher(CipherAlgorithm):
    name = "Fernet"
    category = "Modern"
    requires_key = True
    key_type = "Password"
    security_level = "Modern Authenticated Encryption"
    description = "Uses Fernet authenticated encryption with a password-derived key and a random salt."
    working = [
        "Generate a fresh random salt.",
        "Use scrypt to derive a 256-bit key from the password and salt.",
        "Encrypt and authenticate the message with Fernet.",
        "Store a version marker, salt, and Fernet token in a URL-safe Base64 package.",
        "During decryption, recover the salt, derive the same key, and verify authentication."
    ]
    example = {"input": "Hello", "key": "Strong password", "output": "Randomized token"}

    @staticmethod
    def _derive_key(password, salt):
        if not isinstance(password, str) or not password:
            raise ValueError("Password is required.")
        kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
        return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))

    def encrypt(self, text, key=None):
        salt = os.urandom(16)
        token = Fernet(self._derive_key(key, salt)).encrypt(text.encode("utf-8"))
        package = b"CVF1" + salt + token
        return base64.urlsafe_b64encode(package).decode("ascii")

    def decrypt(self, text, key=None):
        try:
            package = base64.urlsafe_b64decode(text.encode("ascii"))
            if not package.startswith(b"CVF1") or len(package) <= 20:
                raise ValueError
            salt, token = package[4:20], package[20:]
            return Fernet(self._derive_key(key, salt)).decrypt(token).decode("utf-8")
        except (ValueError, InvalidToken, UnicodeEncodeError, UnicodeDecodeError):
            raise ValueError("Decryption failed. Check the password and encrypted data.")
