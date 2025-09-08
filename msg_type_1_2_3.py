"""
type = bit_string[:6]
repeat = bit_string[5:8]
mmsi =  bit_string[8:38]
status = bit_string[38:42]
turn = bit_string[38:42]
speed = bit_string[42:50]
accuracy = bit_string[50:61]
lon = bit_string[61:89]
lat = bit_string[89:116]
course = bit_string[116:128]
heading = bit_string[128:137]
second = bit_string[137:143]
maneuver = bit_string[143:145]
raim = bit_string[145:149]
radio = bit_string[149:]
"""

ais_msg = '!AIVDM,1,1,0,B,139tH:4v@0KmGgtbOq=UKlGd88PDC4h,0*53'
payload = ais_msg.split(',')[5]

def ascii_8b_to_6b(char):
    if char < 96:
        char -= 48
    else:
        char -= 56
    return char&63

def decoge_msg(payload: bytes):
    binary_string = ""
    for char in payload:
        sb = ascii_8b_to_6b(char)
        binary_string += f"{sb:06b}"
    return binary_string

binary_string = decoge_msg(payload.encode('utf-8'))
type = binary_string[:6]
repeat = binary_string[5:8]
mmsi =  binary_string[8:38]
status = binary_string[38:42]
turn = binary_string[38:42]
speed = binary_string[42:50]
accuracy = binary_string[50:61]
lon = binary_string[61:89]
lat = binary_string[89:116]
course = binary_string[116:128]
heading = binary_string[128:137]
second = binary_string[137:143]
maneuver = binary_string[143:145]
raim = binary_string[145:149]
radio = binary_string[149:]
