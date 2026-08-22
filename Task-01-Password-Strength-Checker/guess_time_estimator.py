"""Educational password guess-time estimates.
These values are illustrative, not predictions. Real resistance depends on hashing,
rate limiting, MFA, breach exposure, attacker resources, and attack strategy.
"""
import math

SECONDS_PER_YEAR = 365.25 * 24 * 60 * 60

def format_duration(seconds: float) -> str:
    if seconds < 1:
        return "less than a second"
    units = [
        (60, "second"), (60, "minute"), (24, "hour"),
        (365.25, "day"),
    ]
    value = seconds
    for divisor, name in units:
        if value < divisor:
            return f"{value:.1f} {name}{'' if value == 1 else 's'}"
        value /= divisor
    if value < 1000:
        return f"{value:.1f} years"
    if value < 1_000_000:
        return f"{value/1000:.1f} thousand years"
    return "millions of years+"

def estimate_guess_times(entropy_bits: float, risk_flags=None):
    """Return illustrative average-case estimates for two broad scenarios.
    Online scenario intentionally uses a conservative rate-limited model.
    Offline scenario is a generic high-speed model, not a claim about any
    specific hash algorithm or attack tool.
    """
    if risk_flags and risk_flags.get("common"):
        return {"online": "potentially quickly", "offline": "potentially quickly"}
    if entropy_bits <= 0:
        return {"online": "instantly", "offline": "instantly"}
    # Average guesses ≈ half the search space; cap exponent to avoid float overflow.
    avg_guesses_log2 = max(0.0, entropy_bits - 1.0)
    def seconds_for_rate(rate):
        log2_seconds = avg_guesses_log2 - math.log2(rate)
        if log2_seconds > 1023:
            return float("inf")
        return 2 ** log2_seconds
    online_seconds = seconds_for_rate(10)       # illustrative rate-limited service
    offline_seconds = seconds_for_rate(1e9)     # illustrative high-speed model
    return {
        "online": format_duration(online_seconds),
        "offline": format_duration(offline_seconds),
    }
