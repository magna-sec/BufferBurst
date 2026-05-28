def convert_from_ascii(input_str):
    return input_str.encode("latin-1").hex()


def value_to_hex(value):
    if isinstance(value, str):
        value = int(value, 16)
    return value.to_bytes(4, 'little')


def hex_to_little_endian(hex_string):
    reversed_bytes = bytes.fromhex(hex_string)[::-1]
    return ''.join('\\x{:02x}'.format(b) for b in reversed_bytes)