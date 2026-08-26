from abc import ABC, abstractmethod

class CipherAlgorithm(ABC):
    name = "Base Algorithm"
    category = "Unknown"
    requires_key = False
    key_type = "None"
    security_level = "Unknown"
    description = "No description provided."
    working = []
    example = {}

    @abstractmethod
    def encrypt(self, text: str, key=None) -> str:
        raise NotImplementedError

    @abstractmethod
    def decrypt(self, text: str, key=None) -> str:
        raise NotImplementedError
