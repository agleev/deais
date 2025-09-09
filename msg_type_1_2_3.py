"""
type = bit_string[:6]
repeat = bit_string[5:8]
mmsi =  bit_string[8:38]
status = bit_string[38:42]
turn = bit_string[42:50]
speed = bit_string[50:60]
accuracy = bit_string[60:61]
lon = bit_string[61:89]
lat = bit_string[89:116]
course = bit_string[116:128]
heading = bit_string[128:137]
second = bit_string[137:143]
maneuver = bit_string[143:145]
spare = bit_string[145:148]
raim = bit_string[148:149]
radio = bit_string[149:]
"""

ais_msg = '!AIVDM,1,1,0,B,139tH:4v@0KmGgtbOq=UKlGd88PDC4h,0*53'


import math

def get_lan_lot(val):
    val = bin_to_signed_dec(val)
    return round(val / 600_000, 6)

def get_sog(val):
    val = int(val, 2)
    val = val if (val < 1022) else 1022 
    return val / 10

def bin_to_signed_dec(val):
    n = len(val)
    num = int(val, 2)

    if val[0] == '1':
        mask = (1 << n) - 1
        res = -((num^mask)+1)
    else:
        res = num
    return res

def get_rot(val):
    turn = bin_to_signed_dec(val)
    if not turn:
        return 0
    if abs(turn) in (127, 128):
        return turn
    rot = int(math.sqrt(abs(turn)) * 4.733)
    if turn < 0:
        rot*=-1
    return rot

def get_cog(val):
    cog = int(val, 2)
    cog = cog if (3599 > cog > 0) else 0
    return cog / 10

def get_nav_status(val):
    return int(val, 2)

def get_heading(val):
    hdg = int(val, 2)
    hdg = hdg if (3599 > hdg > 0) else 0
    return hdg

def get_mmsi(val):
    return int(val,2)

def get_msg_type(val):
    return int(val,2)
    
def ascii_8b_to_6b(char):
    if char < 96:
        char -= 48
    else:
        char -= 56
    return char&63

def decode_msg(payload: bytes):
    binary_string = ""
    for char in payload:
        sb = ascii_8b_to_6b(char)
        binary_string += f"{sb:06b}"
    return binary_string
    
def decode_msg_type_1_2_3(ais_msg: str):
    payload = ais_msg.split(',')[5]
    binary_string = decode_msg(payload.encode('utf-8'))
    
    type = get_msg_type(binary_string[:6])
    repeat = binary_string[5:8]
    mmsi =  get_mmsi(binary_string[8:38])
    status = get_nav_status(binary_string[38:42])
    rot = get_rot(binary_string[42:50])
    sog = get_sog(binary_string[50:60])
    accuracy = binary_string[60:61]
    lon = get_lan_lot(binary_string[61:89])
    lat = get_lan_lot(binary_string[89:116])
    cog = get_cog(binary_string[116:128])
    heading = get_heading(binary_string[128:137])
    second = binary_string[137:143]
    maneuver = binary_string[143:145]
    spare = binary_string[145:148]
    raim = binary_string[148:149]
    radio = binary_string[149:]

    return f"""{type};{mmsi};{status};{rot};{sog};{lon};{lat};{cog};{heading}"""

print(decode_msg_type_1_2_3(ais_msg))
