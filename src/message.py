import math
from .decode import (
    bin_to_signed,
    proc_6bit_cha
)            

def get_lan_lot(val:str) -> float:
    """
    Преобразует битовую последовательность в долготу/широту.

    Args:
        val (str): битовая последовательность.

    Returns:
        float: долгота/широта в градусах.
        
    """
    val = bin_to_signed(val)
    return round(val / 600_000, 6)

def get_sog(val:str) -> float:
    """
    Преобразует битовую последовательность в скорость.

    Args:
        val (str): битовая последовательность.

    Returns:
        float: скорость в узлах.
        
    """
    val = int(val, 2)
    val = val if (val < 1022) else 1022 
    return val / 10

def get_rot(val:str) -> float:
    """
    Преобразует битовую последовательность в угловую скорость поворота судна.

    Args:
        val (str): битовая последовательность.

    Returns:
        float: скорость градусы/минута.
        
    """
    turn = bin_to_signed(val)
    if not turn:
        return 0
    if abs(turn) in (127, 128):
        return turn
    rot = int(math.sqrt(abs(turn)) * 4.733)
    if turn < 0:
        rot*=-1
    return rot

def get_cog(val:str) -> float:
    """
    Преобразует битовую последовательность в фактический курс движения судна относительно севера.

    Args:
        val (str): битовая последовательность.

    Returns:
        float: угол в градусах.
        
    """
    cog = int(val, 2)
    cog = cog if (3599 > cog > 0) else 0
    return cog / 10

def get_nav_status(val:str) -> int:
    """
    Преобразует битовую последовательность в навигационный статус судна.

    Args:
        val (str): битовая последовательность.

    Returns:
        int: код статуса.
        
    """
    return int(val, 2)

def get_heading(val:str) -> int:
    """
    Преобразует битовую последовательность в навигационный статус судна.

    Args:
        val (str): битовая последовательность.

    Returns:
        int: код статуса.
        
    """
    hdg = int(val, 2)
    hdg = hdg if (359 > hdg > 0) else 0
    return hdg

def get_shiptype(val:str) -> int:
    """
    Преобразует битовую последовательность в код типа судна.

    Args:
        val (str): битовая последовательность.

    Returns:
        int: код типа судна.
        
    """
    shiptype = int(val, 2)
    shiptype = shiptype if (99 > shiptype > 0) else 0
    return shiptype

def get_draught(val:str) -> float:
    """
    Преобразует битовую последовательность в уровень осадки судна.

    Args:
        val (str): битовая последовательность.

    Returns:
        float: осадка судна в метрах.
        
    """
    draught = int(val, 2)
    return draught/10

def get_mmsi(val:str) -> int:
    """
    Преобразует битовую последовательность в MMSI.

    Args:
        val (str): битовая последовательность.

    Returns:
        int: ID приемника судна в системе  АИС.
        
    """
    return int(val,2)

def get_imo(val:str) -> int:
    """
    Преобразует битовую последовательность в IMO судна.

    Args:
        val (str): битовая последовательность.

    Returns:
        int: ID в реестре Международной морской организации.
        
    """
    return int(val,2)

def get_msg_type(val:str) -> int:
    """
    Преобразует битовую последовательность в тип сообщения АИС.

    Args:
        val (str): битовая последовательность.

    Returns:
        int: тип сообщения АИС.
        
    """
    return int(val,2)

def get_demension_vessel(val:str) -> int:
    """
    Преобразует битовую последовательность в расстояние от
    антены передатчика до носа/кормы/правого и левого бортов судна.

    Args:
        val (str): битовая последовательность.

    Returns:
        float: расстание в метрах.
        
    """
    return int(val,2)

def clear_str_attr(value:str):
    return value.replace("@", "") # 000000 -> "@"

def get_string_field(bit_string:str) -> str:
    """
    Преобразует битовую последовательность в строковые атрибуты судна.

    Args:
        val (str): битовая последовательность.

    Returns:
        str: строка из ASCII-символов.
        
    """
    string_field = proc_6bit_cha(bit_string)
    return clear_str_attr(string_field)

def get_eta(val, threshold):
    """
    Преобразует битовую последовательность в расчетные дату и время прибытия судна.

    Args:
        val (str): битовая последовательность.

    Returns:
        str: отметка минуты/часа/дня/месяца.
        
    """
    eta_attr = int(val, 2)
    eta_attr = eta_attr if eta_attr <= threshold else 0
    return f"{eta_attr:02d}"
    
#MSGS_TYPES
def parse_ais_type_1_2_3(bit_string:str) -> str:
    
    """
    Декомпозиция 1,2 и 3 типов сообщений АИС.
    
    Функция принимает на вход бинарную строку,
    разбивает последовательность бит по заданным правилам
    и преобразует атрибуты данных согласно спецификации
    
    Args:
        binary_data (str): бинарная строка.
    Returns:
        str: строка с атрибутами сообщения.
    
    """ 
    
    type = get_msg_type(bit_string[:6])
    repeat = bit_string[5:8]
    mmsi =  get_mmsi(bit_string[8:38])
    status = get_nav_status(bit_string[38:42])
    rot = get_rot(bit_string[42:50])
    sog = get_sog(bit_string[50:60])
    accuracy = bit_string[60:61]
    lon = get_lan_lot(bit_string[61:89])
    lat = get_lan_lot(bit_string[89:116])
    cog = get_cog(bit_string[116:128])
    heading = get_heading(bit_string[128:137])
    second = bit_string[137:143]
    maneuver = bit_string[143:145]
    spare = bit_string[145:148]
    raim = bit_string[148:149]
    radio = bit_string[149:]

    return f"""{type};{mmsi};{status};{rot};{sog};{lon};{lat};{cog};{heading}"""

def parse_ais_type_5(bit_string:str) -> str:

    """
    Декомпозиция 5 типа сообщения АИС.
    
    Функция принимает на вход бинарную строку,
    разбивает последовательность бит по заданным правилам
    и преобразует атрибуты данных согласно спецификации
    
    Args:
        binary_data (str): бинарная строка.
    Returns:
        str: строка с атрибутами сообщения.
    
    """ 

    type = get_msg_type(bit_string[:6])
    repeat = bit_string[5:8]
    mmsi =  get_mmsi(bit_string[8:38])
    version = bit_string[38:40]
    imo = get_imo(bit_string[40:70])
    callsign = get_string_field(bit_string[70:112])
    shipname = get_string_field(bit_string[112:232])
    shiptype = get_shiptype(bit_string[232:240])
    to_bow = get_demension_vessel(bit_string[240:249])
    to_stern = get_demension_vessel(bit_string[249:258])
    to_port = get_demension_vessel(bit_string[258:264])
    to_starboard = get_demension_vessel(bit_string[264:270])
    epfd = bit_string[270:274]
    
    month = get_eta(bit_string[274:278], threshold=12)
    day = get_eta(bit_string[278:283], threshold=31)
    hour = get_eta(bit_string[283:288], threshold=23)
    minute = get_eta(bit_string[288:294], threshold=59)
    
    draught = get_draught(bit_string[294:302])
    
    destination = get_string_field(bit_string[302:422])
    dte = bit_string[422:423]
    spare = bit_string[423:]

    return f"""{type};{mmsi};{imo};{callsign};{shipname};{shiptype};{to_bow};{to_stern};{to_port};{to_starboard};{month};{day};{hour};{minute};{draught};{destination}"""

    

def parse_ais_type_4_11(bit_string:str) -> str:

    """
    Декомпозиция 4 и 11 типов сообщений АИС.
    
    Функция принимает на вход бинарную строку,
    разбивает последовательность бит по заданным правилам
    и преобразует атрибуты данных согласно спецификации
    
    Args:
        binary_data (str): бинарная строка.
    Returns:
        str: строка с атрибутами сообщения.
    
    """ 
    
    type = get_msg_type(bit_string[:6])
    repeat = bit_string[5:8]
    mmsi =  get_mmsi(bit_string[8:38])

    year = bit_string[38:52]
    month = bit_string[52:56]
    day = bit_string[56:61]
    hour = bit_string[61:66]
    minute = bit_string[66:72]
    second = bit_string[72:78]

    accuracy = bit_string[78:79]
    lon = get_lan_lot(bit_string[79:107])
    lat = get_lan_lot(bit_string[107:134])
    epfd = bit_string[134:138]
    spare = bit_string[138:148]
    raim = bit_string[148:149]
    radio = bit_string[149:]

    return f"""{type};{mmsi};{imo};{lon};{lat}"""

def parse_ais_type_18(bit_string:str) -> str:
    
    """
    Декомпозиция 18 типа сообщения АИС.
    
    Функция принимает на вход бинарную строку,
    разбивает последовательность бит по заданным правилам
    и преобразует атрибуты данных согласно спецификации
    
    Args:
        binary_data (str): бинарная строка.
    Returns:
        str: строка с атрибутами сообщения.
    
    """ 
    type = get_msg_type(bit_string[:6])
    repeat = bit_string[5:8]
    mmsi =  get_mmsi(bit_string[8:38])

    reserved = bit_string[38:46]
    sog = get_sog(bit_string[46:56])
    accuracy = bit_string[56:57]
    lon = get_lan_lot(bit_string[57:85])
    lat = get_lan_lot(bit_string[85:112])
    cog = get_cog(bit_string[112:124])
    heading = get_heading(bit_string[124:133])

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
    
    return f"""{type};{mmsi};{sog};{lon};{lat};{cog};{heading}"""

def parse_ais_type_19(bit_string:str) -> str:

    """
    Декомпозиция 19 типа сообщения АИС.
    
    Функция принимает на вход бинарную строку,
    разбивает последовательность бит по заданным правилам
    и преобразует атрибуты данных согласно спецификации
    
    Args:
        binary_data (str): бинарная строка.
    Returns:
        str: строка с атрибутами сообщения.
    
    """ 

    type = get_msg_type(bit_string[:6])
    repeat = bit_string[5:8]
    mmsi =  get_mmsi(bit_string[8:38])

    reserved = bit_string[38:46]
    sog = get_sog(bit_string[46:56])
    accuracy = bit_string[56:57]
    lon = get_lan_lot(bit_string[57:85])
    lat = get_lan_lot(bit_string[85:112])
    cog = get_cog(bit_string[112:124])
    heading = get_heading(bit_string[124:133])

    second = bit_string[133:139]
    regional = bit_string[139:143]
    shipname = get_string_field(bit_string[143:263])
    shiptype = get_shiptype(bit_string[263:271])

    to_bow = get_demension_vessel(bit_string[271:280])
    to_stern = get_demension_vessel(bit_string[280:289])
    to_port = get_demension_vessel(bit_string[289:295])
    to_starboard = get_demension_vessel(bit_string[295:301])

    epfd = bit_string[301:305]
    raim = bit_string[305:306]
    dte = bit_string[306:307]
    assigned = bit_string[307:308]
    spare = bit_string[308:]
    
    return f"""{type};{mmsi};{sog};{lon};{lat};{cog};{heading};{shipname};{shiptype};{to_bow};{to_stern};{to_port};{to_starboard}"""

def parse_ais_type_24a(bit_string:str) -> str:
    """
    Декомпозиция 24 типа сообщения АИС для судна класса A.
    
    Функция принимает на вход бинарную строку,
    разбивает последовательность бит по заданным правилам
    и преобразует атрибуты данных согласно спецификации
    
    Args:
        binary_data (str): бинарная строка.
    Returns:
        str: строка с атрибутами сообщения.
    
    """    
    
    type = get_msg_type(bit_string[:6])
    repeat = bit_string[5:8]
    mmsi =  get_mmsi(bit_string[8:38])

    partno = bit_string[38:40]
    shipname = get_string_field(bit_string[40:160])
    spare = bit_string[160:]

    return f"""{type};{mmsi};{shipname}"""


def parse_ais_type_24b(bit_string:str) -> str:
    """
    Декомпозиция 24 типа сообщения АИС для судна класса B.
    
    Функция принимает на вход бинарную строку,
    разбивает последовательность бит по заданным правилам
    и преобразует атрибуты данных согласно спецификации
    
    Args:
        binary_data (str): бинарная строка.
    Returns:
        str: строка с атрибутами сообщения.
    
    """    

    type = get_msg_type(bit_string[:6])
    repeat = bit_string[5:8]
    mmsi =  get_mmsi(bit_string[8:38])

    partno = bit_string[38:40]

    shiptype = get_shiptype(bit_string[40:48])

    vendorid = bit_string[48:66]
    model = bit_string[66:70]
    serial = bit_string[70:90]
    callsign = get_string_field(bit_string[90:132])

    to_bow = get_demension_vessel(bit_string[132:141])
    to_stern = get_demension_vessel(bit_string[141:150])
    to_port = get_demension_vessel(bit_string[150:156])
    to_starboard = get_demension_vessel(bit_string[156:162])

    spare = bit_string[162:]
    
    return f"""{type};{mmsi};{shiptype};{callsign};{to_bow};{to_stern};{to_port};{to_starboard}"""

def parse_ais_type_27(bit_string:str) -> str:
    """
    Декомпозиция 27 типа сообщения АИС.
    
    Функция принимает на вход бинарную строку,
    разбивает последовательность бит по заданным правилам
    и преобразует атрибуты данных согласно спецификации
    
    Args:
        binary_data (str): бинарная строка.
    Returns:
        str: строка с атрибутами сообщения.
    
    """
    
    type = get_msg_type(bit_string[:6])
    repeat = bit_string[5:8]
    mmsi =  get_mmsi(bit_string[8:38])

    accuracy = bit_string[38:39]
    raim = bit_string[39:40]
    status = get_nav_status(bit_string[40:44])
    lon = get_lan_lot(bit_string[44:62])
    lat = get_lan_lot(bit_string[62:79])
    sog = get_sog(bit_string[79:85])
    cog = get_cog(bit_string[85:94])
    gnss = bit_string[94:95] 

    return f"""{type};{mmsi};{status};{lon};{lat};{sog};{cog}"""



