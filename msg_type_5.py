"""
#Type 5: Static and Voyage Related Data

type = bit_string[:6]
repeat = bit_string[5:8]
mmsi =  bit_string[8:38]
version = bit_string[38:40]
imo = bit_string[40:70]
callsign = bit_string[70:112]
shipname = bit_string[112:232]
shiptype = bit_string[232:240]
to_bow = bit_string[240:249]
to_stern = bit_string[249:258]
to_port = bit_string[258:264]
to_starboard = bit_string[264:270]
epfd = bit_string[270:274]
month = bit_string[274:278]
day = bit_string[278:283]
hour = bit_string[283:288]
minute = bit_string[288:294]
draught = bit_string[294:302]
destination = bit_string[302:422]
dte = bit_string[422:423]
spare = bit_string[423:]
"""

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


def proc_6bit_chank(binary_string: bytes):
  if len(binary_string) % 6 !=0 :
    raise ValueError

    result=""
    for i in range(0, len(binary_string), 6):
        temp_6b = binary_string[i:i+6]
        ascii_sym = ascii_from_6b(temp_6b)
        result+=ascii_sym
    return result




