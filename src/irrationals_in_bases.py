from mpmath import mp
import math

# Perplexity wrote this

_DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def convert_base(x: float, base: int, frac_places: int) -> str:
    """
    Convert a real number x to a string representation in the given base.
    
    Parameters
    ----------
    x : float
        Number to convert.
    base : int
        Target base (must be >= 2 and <= len(_DIGITS)).
    frac_places : int
        Number of digits after the radix point.
    """
    if base < 2 or base > len(_DIGITS):
        raise ValueError(f"base must be between 2 and {len(_DIGITS)}")
    if frac_places < 0:
        raise ValueError("frac_places must be >= 0")

    # Handle sign
    sign = "-" if x < 0 else ""
    x = abs(x)

    # Integer and fractional parts
    int_part = int(math.floor(x))
    frac = x - int_part

    # Convert integer part
    if int_part == 0:
        int_str = "0"
    else:
        int_digits = []
        n = int_part
        while n > 0:
            n, rem = divmod(n, base)
            int_digits.append(_DIGITS[rem])
        int_digits.reverse()
        int_str = "".join(int_digits)

    # Convert fractional part
    frac_digits = []
    for _ in range(frac_places):
        frac *= base
        digit = int(frac)
        frac_digits.append(_DIGITS[digit])
        frac -= digit

    if frac_places > 0:
        return f"{sign}{int_str}." + "".join(frac_digits)
    else:
        return f"{sign}{int_str}"




pi_base = {
    10 : str(mp.pi),
    7  : convert_base(mp.pi, 7, 50)
}

e_base = {
    10: str(mp.e),
    7 : convert_base(mp.e, 7, 50)
}

phi_base = {
    10: str((1 + mp.sqrt(5)) / 2),
    7 : convert_base((1 + mp.sqrt(5)) / 2, 7, 50)
}