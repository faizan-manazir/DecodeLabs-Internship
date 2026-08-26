import pytest
from algorithms.caesar import CaesarCipher
from algorithms.vigenere import VigenereCipher
from algorithms.atbash import AtbashCipher
from algorithms.rail_fence import RailFenceCipher
from algorithms.xor_cipher import XORCipher
from algorithms.fernet_cipher import FernetCipher
from algorithms.aes_gcm import AESGCMCipher

@pytest.mark.parametrize("cipher,key,text", [
    (CaesarCipher(), "3", "Hello, World! مرحبا 🔐"),
    (VigenereCipher(), "KEY", "Attack at dawn! 123"),
    (AtbashCipher(), None, "Hello, World! مرحبا"),
    (RailFenceCipher(), "3", "WEAREDISCOVEREDFLEEATONCE"),
    (XORCipher(), "secret", "Unicode: مرحبا 你好 🔐"),
    (FernetCipher(), "Strong Password 123!", "Modern crypto 🔐"),
    (AESGCMCipher(), "Strong Password 123!", "Modern crypto 🔐"),
])
def test_round_trip(cipher, key, text):
    encrypted = cipher.encrypt(text, key)
    assert cipher.decrypt(encrypted, key) == text

def test_caesar_known_answer():
    assert CaesarCipher().encrypt("HELLO", "3") == "KHOOR"

def test_vigenere_known_answer():
    assert VigenereCipher().encrypt("HELLO", "KEY") == "RIJVS"

def test_atbash_known_answer():
    assert AtbashCipher().encrypt("HELLO") == "SVOOL"

def test_rail_fence_known_answer():
    cipher = RailFenceCipher()
    assert cipher.encrypt("WEAREDISCOVEREDFLEEATONCE", "3") == "WECRLTEERDSOEEFEAOCAIVDEN"

def test_wrong_modern_password_fails():
    for cipher in (FernetCipher(), AESGCMCipher()):
        encrypted = cipher.encrypt("secret", "correct")
        with pytest.raises(ValueError):
            cipher.decrypt(encrypted, "wrong")

def test_ascii_classical_preserves_non_ascii_letters():
    assert CaesarCipher().encrypt("é你好", "5") == "é你好"

def test_invalid_rail_key():
    with pytest.raises(ValueError):
        RailFenceCipher().encrypt("hello", "1")
