def convert_from_ascii(input_str):
    """
    """
    # Convert each character in the input string to its ASCII value
    ascii_values = [ord(char) for char in input_str]
    
    # Convert the ASCII values to hexadecimal representation
    hex_values = [hex(value)[2:].zfill(2) for value in ascii_values]
    
    # Concatenate the hexadecimal values to form the final representation
    hex_string = ''.join(hex_values)
    
    return hex_string


def value_to_hex(value):
    byte_string = b""
    # Convert value to integer if it's a string
    if isinstance(value, str):
        value = int(value, 16)

    # Convert the value to little-endian hex
    little_endian_hex = value.to_bytes(4, 'little').hex()

    # Convert little-endian hex to bytes and append to the byte string
    byte_string += bytes.fromhex(little_endian_hex)

    return byte_string


def hex_to_little_endian(hex_string):
    # Convert hexadecimal string to bytes
    byte_data = bytes.fromhex(hex_string)

    # Reverse the byte order
    reversed_byte_data = byte_data[::-1]

    # Format the bytes as a string
    formatted_string = ''.join('\\x{:02x}'.format(byte) for byte in reversed_byte_data)

    return formatted_string