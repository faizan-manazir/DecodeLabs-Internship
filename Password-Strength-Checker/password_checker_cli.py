"""
password_checker_cli.py
DecodeLabs Cyber Security Project 1 - Password Security Analyzer (CLI)

Command-line interface. Demonstrates that the analysis logic in
password_analyzer.py works completely independently of the GUI.

The password is read with getpass so it is never echoed to the
terminal, and it is analyzed only in memory - it is never written
to a file or log.
"""

import getpass
import sys

from password_analyzer import analyze_password, load_common_passwords

BAR_WIDTH = 30


def print_header():
    print("=" * 36)
    print("    PASSWORD SECURITY ANALYZER")
    print("=" * 36)
    print()


def render_bar(score, width=BAR_WIDTH):
    filled = round((score / 100) * width)
    return "#" * filled + "-" * (width - filled)


def print_result(result):
    print()
    print(f"Score: {result['score']}/100")
    print(f"[{render_bar(result['score'])}]")
    print(f"Strength: {result['strength'].upper()}")
    print(f"Estimated Entropy: {result['entropy_bits']} bits "
          f"(estimate only, not an absolute measure of security)")
    print()

    checks = result["checks"]
    risk_flags = result["risk_flags"]

    print("CHECKS:")
    _print_check("Good password length (8+ chars)", checks["length_ok"])
    _print_check("Contains uppercase letters", checks["uppercase"])
    _print_check("Contains lowercase letters", checks["lowercase"])
    _print_check("Contains numbers", checks["number"])
    _print_check("Contains special characters", checks["special"])
    _print_check("Not a known common password", not risk_flags["common"])
    _print_check("No repeated-character pattern", not risk_flags["repeated"])
    _print_check("No sequential pattern (e.g. 1234, abcd)", not risk_flags["sequential"])
    _print_check("No keyboard-walk pattern (e.g. qwerty)", not risk_flags["keyboard"])

    print()
    print("RECOMMENDATIONS:")
    for rec in result["recommendations"]:
        print(f"- {rec}")
    print()


def _print_check(label, passed):
    mark = "[OK]" if passed else "[!! ]"
    print(f"{mark} {label}")


def main():
    print_header()
    common_set = load_common_passwords()

    try:
        password = getpass.getpass("Enter password (hidden): ")
    except (EOFError, KeyboardInterrupt):
        print("\nNo password entered. Exiting.")
        sys.exit(0)

    if password == "":
        print("\nNo password entered.")
        sys.exit(0)

    result = analyze_password(password, common_set)

    # The plaintext password is discarded here - only the structured
    # result (score/strength/checks/recommendations) is used from now on.
    del password

    print_result(result)


if __name__ == "__main__":
    main()
