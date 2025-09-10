import math
from .decode import (
    bin_to_signed_dec,
    proc_6bit_cha
)

def get_lan_lot(val):
    val = bin_to_signed_dec(val)
    return round(val / 600_000, 6)

def get_sog(val):
    val = int(val, 2)
    val = val if (val < 1022) else 1022 
    return val / 10

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


def clear_str_attr(value:str):
    return value.replace("@", "") # 000000 -> "@"

def get_vessel_name(binary_string: bytes):
    vessel_name = proc_6bit_cha(binary_string)
    return clear_str_attr(vessel_name)


    

#MSGS_TYPES
def decode_msg_type_1_2_3(binary_string: str):
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



def decode_msg_type_5(binary_string: str):
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
    pass

def decode_msg_type_4_11():
    """
    #Type 4: Base Station Report
    #Type 11: UTC/Date Response

    type = bit_string[:6]
    repeat = bit_string[5:8]
    mmsi =  bit_string[8:38]

    year = bit_string[38:52]
    month = bit_string[52:56]
    day = bit_string[56:61]
    hour = bit_string[61:66]
    minute = bit_string[66:72]
    second = bit_string[72:78]

    accuracy = bit_string[78:79]
    lon = bit_string[79:107]
    lat = bit_string[107:134]
    epfd = bit_string[134:138]
    spare = bit_string[138:148]
    raim = bit_string[148:149]
    radio = bit_string[149:]

    """
    
    
    pass

def decode_msg_type_18():
    """
    #Type 18: Standard Class B CS Position Report

    type = bit_string[:6]
    repeat = bit_string[5:8]
    mmsi =  bit_string[8:38]

    reserved = bit_string[38:46]
    sog = bit_string[46:56]
    accuracy = bit_string[56:57]
    lon = bit_string[57:85]
    lat = bit_string[85:112]
    cog = bit_string[112:124]
    heading = bit_string[124:133]

    second = bit_string[133:139]
    regional = bit_string[139:141]
    cs = bit_string[141:142]
    display = bit_string[142:143]
    dsc = bit_string[143:144]
    band = bit_string[144:145]
    msg22 = bit_string[145:146]
    assigned = bit_string[146:147]
    raim = bit_string[147:148]
    radio = bit_string[148:]

    """
    pass


def decode_msg_type_19():
    """
    Type 19: Extended Class B CS Position Report

    type = bit_string[:6]
    repeat = bit_string[5:8]
    mmsi =  bit_string[8:38]

    reserved = bit_string[38:46]
    sog = bit_string[46:56]
    accuracy = bit_string[56:57]
    lon = bit_string[57:85]
    lat = bit_string[85:112]
    cog = bit_string[112:124]
    heading = bit_string[124:133]

    second = bit_string[133:139]
    regional = bit_string[139:143]
    shipname = bit_string[143:263]
    shiptype = bit_string[263:271]

    to_bow = bit_string[271:280]
    to_stern = bit_string[280:289]
    to_port = bit_string[289:295]
    to_starboard = bit_string[295:301]

    epfd = bit_string[301:305]
    raim = bit_string[305:306]
    dte = bit_string[306:307]
    assigned = bit_string[307:308]
    spare = bit_string[308:]
    """
    
    pass

def decode_msg_type_24a():
    """
    #Type 24A: Static Data Report

    type = bit_string[:6]
    repeat = bit_string[5:8]
    mmsi =  bit_string[8:38]

    partno = bit_string[38:40]
    shipname = bit_string[40:160]
    spare = bit_string[160:]


    """
    pass


def decode_msg_type_24b():
    """
    #Type 24B: Static Data Report

    type = bit_string[:6]
    repeat = bit_string[5:8]
    mmsi =  bit_string[8:38]

    partno = bit_string[38:40]

    shiptype = bit_string[40:48]

    vendorid = bit_string[48:66]
    model = bit_string[66:70]
    serial = bit_string[70:90]
    callsign = bit_string[90:132]

    to_bow = bit_string[132:141]
    to_stern = bit_string[141:150]
    to_port = bit_string[150:156]
    to_starboard = bit_string[156:162]

    spare = bit_string[162:]

    """
    pass



def decode_msg_type_27():
    """
    #Type 27: Long Range AIS Broadcast message

    type = bit_string[:6]
    repeat = bit_string[5:8]
    mmsi =  bit_string[8:38]

    accuracy = bit_string[38:39]
    raim = bit_string[39:40]
    status = bit_string[40:44]
    lon = bit_string[44:62]
    lat = bit_string[62:79]
    sog = bit_string[79:85]
    course = bit_string[85:94]
    gnss = bit_string[94:95] 
    spare = bit_string[95:] 
    """
    pass