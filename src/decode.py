

ais_msg = '!AIVDM,1,1,0,B,139tH:4v@0KmGgtbOq=UKlGd88PDC4h,0*53'

ascii_6_dict = {
    0: '@',   1: 'A',   2: 'B',   3: 'C',   4: 'D',   5: 'E',   6: 'F',   7: 'G',
    8: 'H',   9: 'I',  10: 'J',  11: 'K',  12: 'L',  13: 'M',  14: 'N',  15: 'O',
    16: 'P',  17: 'Q',  18: 'R',  19: 'S',  20: 'T',  21: 'U',  22: 'V',  23: 'W',
    24: 'X',  25: 'Y',  26: 'Z',  27: '[',  28: '\\', 29: ']',  30: '^',  31: '_',
    32: ' ',  33: '!',  34: '"',  35: '#',  36: '$',  37: '%',  38: '&',  39: "'",
    40: '(',  41: ')',  42: '*',  43: '+',  44: ',',  45: '-',  46: '.',  47: '/',
    48: '0',  49: '1',  50: '2',  51: '3',  52: '4',  53: '5',  54: '6',  55: '7',
    56: '8',  57: '9',  58: ':',  59: ';',  60: '<',  61: '=',  62: '>',  63: '?'
}

def get_ascii(value:str) -> str:
    """
    Converts a binary string to ASCII character.

    The function takes a binary string as input, converts it to an integer,
    extracts the least significant 6 bits (via bitwise AND operation) and returns the character
    from the ascii_6_dict dictionary.

    Args:
        value (str): Binary string (e.g., "000010", "010100")
    Returns:
        str: ASCII character from the ascii_6_dict dictionary.

    Example:
        >>> get_ascii("000010")
        'B'
        
        >>> get_ascii("010100")
        'T'
        
    """
    idx = int(value, 2)
    return ascii_6_dict[idx&63]


def proc_6bit_cha(binary_data: str) -> str:
    """
    Decodes binary data from 6-bit sequence to a string of ASCII characters.

    The function takes a binary string as input, splits it into 6-bit blocks and 
    converts each block to ASCII character using the get_ascii() function.

    Args:
        binary_data (str): Binary string (e.g., "000010010100")
    Returns:
        str: String of ASCII characters.

    Example:
        >>> proc_6bit_cha("000010010100")
        'BT'
        
    """
    if len(binary_data) % 6 !=0 :
        raise ValueError

    result=""
    for i in range(0, len(binary_data), 6):
        temp_6b = binary_data[i:i+6]
        ascii_sym = get_ascii(temp_6b)
        result+=ascii_sym
    return result

def bin_to_signed(val: str) -> int:
    """
    Converts a binary string to a signed decimal number.

    The function takes a binary string as input, determines the sign of the number by the most significant bit,
    converts to negative decimal representation.

    Args:
        val (str): Binary string, the most significant bit determines the sign.
    Returns:
        int: Signed decimal number.

    Example:
        >>> bin_to_signed("1010110011110101101101001011")
        -87073973
        
        >>> bin_to_signed("0010110011110101101101001011")
        47143755
        
    """
    n = len(val)
    num = int(val, 2)

    if val[0] == '1':
        mask = (1 << n) - 1
        res = -((num^mask)+1)
    else:
        res = num
    return res

def bit_shifts(b:int, shift:int=0):
    """
    Bitwise right shift of a number.

    The function takes a numeric value b as input
    and shift - the number of least significant bits to ignore
    up to the nearest 6-bit boundary.

    Args:
        b (int): Numeric value to process.
        shift (int): Number of padding bits.
    Returns:
        str: Binary string

    Example:
        >>> bit_shifts(43, 2)
        '1010'
        
        >>> bit_shifts(23, 3)
        '010'
        
    """
    b = b >> shift
    return f"{b:b}".zfill(6-shift)

def ascii_8b_to_6b(char:int) -> int:
    """
    Converts 8-bit ASCII character code to 6-bit value.
    
    The function takes a numeric code from the 8-bit ASCII character table
    and converts it to a number from the 6-bit ASCII character table according to the given rule.
    
    Args:
        char (int): ASCII character code in range 0-255 
    Returns:
        int: 6-bit value in range 0-63
        
    Example:
        >>> ascii_8b_to_6b(48)
        0
        
        >>> ascii_8b_to_6b(57)
        9
        
    """
    if char < 96:
        char -= 48
    else:
        char -= 56
    return char&63

def decode_msg(payload: bytes, shift:int = 0) -> str:
    """
    Decoding raw AIS message to binary string with 6-bit conversion.

    Args:
        payload (bytes): Part of AIS message with ship data payload.
        shift (int): Shift parameter for processing the last 6 bits.

    Returns:
        str: Decoded binary string

    Example:
        >>> decode_msg(b"139tH:4v@0KmGgtbOq=UKlGd88PDC4h")
        '000001000011001001111100011000001010000100111110010000000\
        0000110111101010101111011111111001010100111111110010011011\
        00101011011110100010111101100001000001000100000010100010011000100110000'
    """
    binary_string = ""
    for idx, char in enumerate(payload):
        sb = ascii_8b_to_6b(char)
        if idx == (len(payload) - 1) and shift:
            sb = bit_shifts(sb)
            binary_string += sb
        else:
            binary_string += f"{sb:06b}"
    return binary_string
