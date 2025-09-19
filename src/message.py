from functools import wraps

from src.values import *

    
register_types = {}

def register_func(msg_type):
    """
    Декоратор для регистрации функции-обработчика для определенного типа данных.

    Args:
        msg_type (int): тип сообщения АИС.
    """
    def deco(func):
        register_types[msg_type] = func
        return func
    return deco

def call(msg_type,*args,**kwargs):
    if msg_type not in register_types:
        raise ValueError
    return register_types[msg_type](*args,**kwargs)


@register_func(1)
@register_func(2)
@register_func(3)
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

@register_func(5)
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

@register_func(4)
@register_func(11)
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

    return f"""{type};{mmsi};{lon};{lat}"""

@register_func(18)
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

@register_func(19)
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

@register_func('24a')
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

@register_func('24b')
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

@register_func(27)
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
