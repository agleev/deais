import math

from src.decode import (
    bin_to_signed,
    proc_6bit_cha
)            

def get_lon_lat(val:str) -> float:
    """
    Converts a bit sequence to latitude/longitude.
    
    Args:
        val (str): Bit sequence.
    Returns:
        float: Latitude/longitude in degrees.
        
    """
    val = bin_to_signed(val)
    return round(val / 600_000, 6)

def get_sog(val:str) -> float:
    """
    Converts a bit sequence to speed over ground.
    
    Args:
        val (str): Bit sequence.
    Returns:
        float: Speed in knots.
        
    """
    val = int(val, 2)
    val = val if (val < 1022) else 1022 
    return val / 10

def get_rot(val:str) -> float:
    """
    Converts a bit sequence to vessel's rate of turn.
    
    Args:
        val (str): Bit sequence.
    Returns:
        float: Turn rate in degrees per minute.
        
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
    Converts a bit sequence to course over ground relative to true north.
    
    Args:
        val (str): Bit sequence.
    Returns:
        float: Angle in degrees.
        
    """
    cog = int(val, 2)
    cog = cog if (3599 > cog > 0) else 0
    return cog / 10

def get_nav_status(val:str) -> int:
    """
    Converts a bit sequence to vessel's navigation status.
    
    Args:
        val (str): Bit sequence.
    Returns:
        int: Status code.
        
    """
    return int(val, 2)

def get_heading(val:str) -> int:
    """
    Converts a bit sequence to vessel's true heading.
    
    Args:
        val (str): Bit sequence.
    Returns:
        int: Heading in degrees.
        
    """
    hdg = int(val, 2)
    hdg = hdg if (359 > hdg > 0) else 0
    return hdg

def get_shiptype(val:str) -> int:
    """
    Converts a bit sequence to vessel type code.
    
    Args:
        val (str): Bit sequence.
    Returns:
        int: Vessel type code.
        
    """
    shiptype = int(val, 2)
    shiptype = shiptype if (100 > shiptype > 0) else 0
    return shiptype

def get_draught(val:str) -> float:
    """
    Converts a bit sequence to vessel's draught level.
    
    Args:
        val (str): Bit sequence.
    Returns:
        float: Vessel draught in meters.
        
    """
    draught = int(val, 2)
    return draught/10

def get_mmsi(val:str) -> int:
    """
    Converts a bit sequence to MMSI (Maritime Mobile Service Identity).
    
    Args:
        val (str): Bit sequence.
    Returns:
        int: Vessel receiver ID in AIS system.
        
    """
    return int(val,2)

def get_imo(val:str) -> int:
    """
    Converts a bit sequence to vessel's IMO number.
    
    Args:
        val (str): Bit sequence.
    Returns:
        int: ID in International Maritime Organization registry.
        
    """
    return int(val,2)

def get_msg_type(val:str) -> int:
    """
    Converts a bit sequence to AIS message type.
    
    Args:
        val (str): Bit sequence.
    Returns:
        int: AIS message type.
        
    """
    return int(val,2)

def get_demension_vessel(val:str) -> int:
    """
    Converts a bit sequence to distance from transmitter antenna
    to bow/stern/port/starboard sides of the vessel.
    
    Args:
        val (str): Bit sequence.
    Returns:
        int: Distance in meters.
        
    """
    return int(val,2)

def clear_str_attr(value:str):
    """
    Cleans string attributes by removing '@' characters.
    
    Args:
        value (str): String to clean.
    Returns:
        str: Cleaned string.
    """
    return value.replace("@", "") # 000000 -> "@"

def get_string_field(bit_string:str) -> str:
    """
    Converts a bit sequence to vessel's string attributes.
    
    Args:
        bit_string (str): Bit sequence.
    Returns:
        str: String of ASCII characters.
        
    """
    string_field = proc_6bit_cha(bit_string)
    return clear_str_attr(string_field)

def get_eta(val, threshold) -> str:
    """
    Converts a bit sequence to estimated time of arrival (ETA).
    
    Args:
        val (str): Bit sequence.
        threshold (int): Maximum allowed value for the ETA component.
    Returns:
        str: Formatted minute/hour/day/month.
        
    """
    eta_attr = int(val, 2)
    eta_attr = eta_attr if eta_attr <= threshold else 0
    return f"{eta_attr:02d}"
