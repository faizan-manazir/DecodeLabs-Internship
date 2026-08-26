from algorithms.caesar import CaesarCipher
from algorithms.vigenere import VigenereCipher
from algorithms.atbash import AtbashCipher
from algorithms.rail_fence import RailFenceCipher
from algorithms.xor_cipher import XORCipher
from algorithms.fernet_cipher import FernetCipher
from algorithms.aes_gcm import AESGCMCipher

class CryptoService:
    def __init__(self):
        self.algorithms = {
            "caesar": CaesarCipher(), "vigenere": VigenereCipher(),
            "atbash": AtbashCipher(), "rail_fence": RailFenceCipher(),
            "xor": XORCipher(), "fernet": FernetCipher(),
            "aes_gcm": AESGCMCipher()
        }

    def get_algorithms_info(self):
        return {
            key: {
                "name": algo.name, "category": algo.category,
                "requires_key": algo.requires_key, "key_type": algo.key_type,
                "security_level": algo.security_level,
                "description": algo.description, "working": algo.working,
                "example": algo.example
            }
            for key, algo in self.algorithms.items()
        }

    def _get(self, algorithm_id, key):
        if algorithm_id not in self.algorithms:
            raise ValueError("Unknown algorithm.")
        algo = self.algorithms[algorithm_id]
        if algo.requires_key and not key:
            raise ValueError(f"{algo.name} requires a key.")
        return algo

    def encrypt(self, algorithm_id, text, key=None):
        return self._get(algorithm_id, key).encrypt(text, key)

    def decrypt(self, algorithm_id, text, key=None):
        return self._get(algorithm_id, key).decrypt(text, key)
