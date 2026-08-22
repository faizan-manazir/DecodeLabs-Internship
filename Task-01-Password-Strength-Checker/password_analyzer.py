"""
password_analyzer.py
DecodeLabs Cyber Security Project 1 - Password Security Analyzer

Core analysis engine. Contains all password-strength logic used by
both the GUI (password_checker_gui.py) and CLI (password_checker_cli.py)
front ends.

SECURITY NOTE:
This module analyzes passwords entirely in memory. It never writes a
password to disk, a log file, or a network socket. Only the small,
static list of known common passwords is read from disk.
"""

import re
import math
import os

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

COMMON_PASSWORDS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "common_passwords.txt"
)

# Common keyboard-walk patterns (checked as substrings, forwards & backwards)
KEYBOARD_PATTERNS = [
    "qwertyuiop", "qwerty", "asdfghjkl", "asdfgh", "asdf",
    "zxcvbnm", "zxcvbn", "zxcv", "qazwsx", "wsxedc",
    "1qaz2wsx", "qweasd", "poiuyt", "mnbvcx",
]

REPEATED_CHAR_THRESHOLD = 4     # e.g. "aaaa", "1111", "$$$$"
SEQUENTIAL_MIN_LENGTH = 4       # e.g. "1234", "abcd", "4321", "dcba"


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_common_passwords(path=COMMON_PASSWORDS_PATH):
    """Load the common-password wordlist into a lowercase set."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return {line.strip().lower() for line in f if line.strip()}
    except FileNotFoundError:
        # Fail safe: analyzer still works, common-password check just
        # won't flag anything if the wordlist is missing.
        return set()


# ---------------------------------------------------------------------------
# Basic character checks
# ---------------------------------------------------------------------------

def has_lowercase(password):
    return bool(re.search(r"[a-z]", password))


def has_uppercase(password):
    return bool(re.search(r"[A-Z]", password))


def has_number(password):
    return bool(re.search(r"\d", password))


def has_special(password):
    return bool(re.search(r"[^A-Za-z0-9]", password))


# ---------------------------------------------------------------------------
# Risk pattern checks
# ---------------------------------------------------------------------------

def normalize_common_candidate(password):
    """Normalize simple human variations for educational common-password checks.
    This is intentionally conservative and does not claim to detect breached passwords.
    """
    candidate = password.strip().lower()
    candidate = re.sub(r"[^a-z0-9]+$", "", candidate)
    return candidate


def is_common_password(password, common_set):
    candidate = password.lower()
    normalized = normalize_common_candidate(password)
    return candidate in common_set or normalized in common_set


def has_repeated_characters(password, threshold=REPEATED_CHAR_THRESHOLD):
    """Detects a single character repeated `threshold` or more times in a row,
    e.g. 'aaaa', '1111', '$$$$'."""
    pattern = r"(.)\1{" + str(threshold - 1) + r",}"
    return bool(re.search(pattern, password))


def has_sequential_pattern(password, min_length=SEQUENTIAL_MIN_LENGTH):
    """Detects predictable ascending/descending sequences such as
    '1234', 'abcd', '4321', 'dcba'."""
    pw = password.lower()
    n = len(pw)
    if n < min_length:
        return False

    for i in range(n - min_length + 1):
        chunk = pw[i:i + min_length]
        if not chunk.isalnum():
            continue

        ascending = all(
            ord(chunk[j + 1]) - ord(chunk[j]) == 1 for j in range(len(chunk) - 1)
        )
        descending = all(
            ord(chunk[j]) - ord(chunk[j + 1]) == 1 for j in range(len(chunk) - 1)
        )
        if ascending or descending:
            return True
    return False


def has_keyboard_pattern(password, patterns=KEYBOARD_PATTERNS):
    """Detects common keyboard-walk patterns such as 'qwerty', 'asdf', 'zxcv'."""
    pw = password.lower()
    for pattern in patterns:
        if pattern in pw or pattern[::-1] in pw:
            return True
    return False


# ---------------------------------------------------------------------------
# Entropy estimation
# ---------------------------------------------------------------------------

def estimate_entropy(password):
    """Rough entropy estimate in bits, based on character-pool size and length.

    This is an ESTIMATE only. It assumes characters are drawn uniformly
    at random from the pool implied by the character classes present,
    which is not true for human-chosen passwords. It should be treated
    as a rough indicator, not an absolute measure of security.
    """
    pool = 0
    if has_lowercase(password):
        pool += 26
    if has_uppercase(password):
        pool += 26
    if has_number(password):
        pool += 10
    if has_special(password):
        pool += 33  # approx. printable ASCII symbols

    if pool == 0 or len(password) == 0:
        return 0.0

    return round(len(password) * math.log2(pool), 1)


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def calculate_score(password, common_set):
    """Calculates a 0-100 security score and returns the risk flags used
    to compute it."""
    score = 0
    length = len(password)

   if length >= 8:
    score += 10
   if length >= 12:
    score += 15
   if length >= 16:
    score += 15
   if length >= 20:
    score += 15
   if length >= 24:
    score += 5

    if has_lowercase(password):
        score += 10
    if has_uppercase(password):
        score += 10
    if has_number(password):
        score += 10
    if has_special(password):
        score += 10

    common = is_common_password(password, common_set)
    repeated = has_repeated_characters(password)
    sequential = has_sequential_pattern(password)
    keyboard = has_keyboard_pattern(password)

    if common:
        score -= 40
    if repeated:
        score -= 15
    if sequential:
        score -= 15
    if keyboard:
        score -= 15

    score = max(0, min(100, score))

    risk_flags = {
        "common": common,
        "repeated": repeated,
        "sequential": sequential,
        "keyboard": keyboard,
    }
    return score, risk_flags


def classify_strength(score, risk_flags=None):
    # A detected common password should never receive a high-strength label.
    if risk_flags and risk_flags.get("common"):
        return "Weak"
    if score >= 85:
        return "Very Strong"
    elif score >= 65:
        return "Strong"
    elif score >= 40:
        return "Medium"
    else:
        return "Weak"


# ---------------------------------------------------------------------------
# Recommendations
# ---------------------------------------------------------------------------

def generate_recommendations(password, checks, risk_flags):
    recs = []

    if len(password) < 12:
        recs.append("Increase the password length to at least 12 characters.")
    if not checks["lowercase"]:
        recs.append("Add a lowercase letter.")
    if not checks["uppercase"]:
        recs.append("Add an uppercase letter.")
    if not checks["number"]:
        recs.append("Add a number.")
    if not checks["special"]:
        recs.append("Add a special character (e.g. !, @, #, $).")
    if risk_flags["common"]:
        recs.append("Avoid commonly used passwords.")
    if risk_flags["repeated"]:
        recs.append("Avoid repeating the same character multiple times in a row.")
    if risk_flags["sequential"]:
        recs.append("Avoid predictable sequences (e.g. 1234, abcd).")
    if risk_flags["keyboard"]:
        recs.append("Avoid common keyboard patterns (e.g. qwerty, asdf).")

    if not recs:
        recs.append("Consider using a longer, unique passphrase for extra security.")

    return recs


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def analyze_password(password, common_set=None):
    """Analyzes a single password and returns a structured result dict.

    The password is analyzed entirely in memory and is never written
    to disk, logged, or transmitted anywhere by this function.
    """
    if common_set is None:
        common_set = load_common_passwords()

    checks = {
        "length_ok": len(password) >= 8,
        "lowercase": has_lowercase(password),
        "uppercase": has_uppercase(password),
        "number": has_number(password),
        "special": has_special(password),
    }

    score, risk_flags = calculate_score(password, common_set)
    strength = classify_strength(score, risk_flags)
    entropy = estimate_entropy(password)
    recommendations = generate_recommendations(password, checks, risk_flags)

    # Important rule: a known common password must not be rated Strong or
    # Very Strong just because it happens to contain multiple character
    # types (e.g. "Password123!").
    if risk_flags["common"] and strength in ("Strong", "Very Strong"):
        strength = "Weak"
        score = min(score, 30)

    return {
        "password_length": len(password),
        "score": score,
        "strength": strength,
        "entropy_bits": entropy,
        "checks": checks,
        "risk_flags": risk_flags,
        "recommendations": recommendations,
    }


if __name__ == "__main__":
    # Quick manual smoke test when running this file directly.
    samples = ["123456", "password", "abcdefgh", "AAAA1111",
               "Hello123", "MySecure!Pass2026#Example"]
    common = load_common_passwords()
    for pw in samples:
        result = analyze_password(pw, common)
        print(f"{pw!r:30} -> score={result['score']:3} "
              f"strength={result['strength']:<12} "
              f"entropy={result['entropy_bits']} bits")
