import struct

_ALPHABET = b"abcdefghijklmnopqrstuvwxyz"


def _de_bruijn(alphabet: bytes, n: int) -> bytes:
    k = len(alphabet)
    a = bytearray(k * n)
    seq: list[int] = []

    def db(t: int, p: int):
        if t > n:
            if n % p == 0:
                seq.extend(a[1:p + 1])
        else:
            a[t] = a[t - p]
            db(t + 1, p)
            for j in range(a[t - p] + 1, k):
                a[t] = j
                db(t + 1, t)

    db(1, 1)
    return bytes(alphabet[i] for i in seq)


# 26^4 = 456,976 bytes — enough for any standard BOF exercise
_PATTERN: bytes = _de_bruijn(_ALPHABET, 4)


def cyclic(length: int) -> bytes:
    if length > len(_PATTERN):
        raise ValueError(f"Requested pattern length {length} exceeds max {len(_PATTERN)}")
    return _PATTERN[:length]


def cyclic_find(eip: str) -> int:
    """
    Find the offset of an EIP value in the cyclic pattern.
    eip: hex string as read from the debugger, e.g. '64636261' or '0x64636261'.
    Returns offset into the pattern, or -1 if not found.
    """
    eip = eip.strip().lower().lstrip("0x").replace(" ", "")
    if len(eip) != 8:
        return -1
    # On x86 the CPU loads EIP little-endian from the stack.
    # If EIP = 0x64636261 the bytes we wrote were: \x61\x62\x63\x64 = "abcd"
    search = struct.pack("<I", int(eip, 16))
    return _PATTERN.find(search)
