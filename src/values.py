import math

from src.decode import (
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
    shiptype = shiptype if (100 > shiptype > 0) else 0
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