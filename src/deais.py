from typing import Union, List, Tuple
import message
from decode import decode_msg
from values import get_msg_type

def get_msg_parts(raw: str):
    return raw.split(",")


def preproc_multipart_msg(messages: Union[str, List[str]]) -> Tuple[str, int]:
    """
    Assemble multipart AIS message from fragments.
    
    Args:
        messages: Single message string or list of message fragments
    Returns:
        Assembled payload and fill bits for the last fragment
    Raises:
        ValueError: If messages are invalid or incomplete
    """

    if isinstance(messages, str):
        messages = [messages]
    
    parts = {}
    total_parts = 0
    message_id = None
    for message in messages:

        (package_name,
        cfrags, nfrag,
        seq, ab_code,
        payload, shift_sum) = get_msg_parts(message)
        
        cfrags = int(cfrags)
        nfrag = int(nfrag)
        
        if not package_name.startswith('!AIVDM'):
            raise ValueError
            
        parts[nfrag] = payload
        total_parts = cfrags
    
    payloads = ""
    for i in range(1, total_parts + 1):
        if i in parts:
            payloads += parts[i]
        else:
            raise ValueError(f"No found part of message, total: {total_parts}")
    

    shift = shift_sum.split('*')[0]
    try:
        shift = int(shift)
    except ValueError:
        shift = 0
    
    return payloads, shift
    
def ais_decode(raw: Union[str, List[str]]) -> str:
    """
    Decoding AIS Message for NMEA 0183 standard.

    The function accepts an AIS message as input, decodes each character into a binary str (according to a 6-bit ASCII table).
    The bit sequence is split according to the specified rules (according to the message type) and the values of the message fields are extracted.
    
    Args:
        raw: Raw NMEA message string
    Returns:
        Parsed NMEA message object
    Raises:
        ValueError: If message format is invalid
    """
    if not raw:
        return ValueError(f"Empty message: {raw}")
    
    payload, shift = preproc_multipart_msg(raw)
    binary_string = decode_msg(payload.encode(), shift)
    msg_type = get_msg_type(binary_string[:6])
    msg_values = message.call(msg_type, binary_string)
    return msg_values
