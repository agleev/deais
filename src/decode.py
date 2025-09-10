

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

def get_ascii(value):
    idx = int(value, 2)
    return ascii_6_dict[idx&63]


def proc_6bit_cha(binary_string: bytes):
    if len(binary_string) % 6 !=0 :
        raise ValueError

    result=""
    for i in range(0, len(binary_string), 6):
        temp_6b = binary_string[i:i+6]
        ascii_sym = get_ascii(temp_6b)
        result+=ascii_sym
    return result

def bin_to_signed_dec(val):
    n = len(val)
    num = int(val, 2)

    if val[0] == '1':
        mask = (1 << n) - 1
        res = -((num^mask)+1)
    else:
        res = num
    return res

def bit_shifts(b, shift):
    b = b >> shift
    return f"{b}".zfill(6-shift)

def ascii_8b_to_6b(char):
    if char < 96:
        char -= 48
    else:
        char -= 56
    return char&63

def decode_msg(payload: bytes, shift:int = 0):
    binary_string = ""
    for idx, char in enumerate(payload):
        sb = ascii_8b_to_6b(char)
        if idx == (len(payload) - 1) and shift:
            sb = bit_shifts(sb)
            binary_string += sb
        else:
            binary_string += f"{sb:06b}"
    return binary_string
