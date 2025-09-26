from typing import Union, List, Tuple
import message
from decode import decode_msg
from values import get_msg_type

def get_msg_parts(raw: str):
    return raw.split(",")


def preproc_multipart_msg(messages: Union[str, List[str]]) -> Tuple[str, int]:
    """
    Разбивка сообщения на составные части.

    Функция принимает на вход сообщение (или части сообщения) АИС,
    вовзвращает полезную нагрузку сообщения и количество битов заполнения для последних 6 бит сообщения.
    
    Args:
        messages (str), list(str): строка или коллекция строк из нескольких частей одного сообщения.
    Returns:
        payloads (str): полезная нагрузка сообщения АИС с данными о судне.
        shift (int): количество младших битов, которые нужно игнорировать.
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
    Декодирует сообщение АИС стандарта NMEA 0183.

    Функция принимает на вход сообщение АИС, декодирует каждый символ в бинарное представление (в соответсвии 6-битной таблицы ASCII).
    Битовая последовательность разбивается по заданным правилам (согласно типу сообщения) и извлекаются значения полей сообщения.
    
    Args:
        raw (str), list(str): строка или коллекция строк из нескольких частей одного сообщения.
    Returns:
        msg_values (str): строка декодированного сообщения.
    """
    if not raw:
        return ValueError(f"Empty message: {raw}")
    
    payload, shift = preproc_multipart_msg(raw)
    binary_string = decode_msg(payload.encode(), shift)
    msg_type = get_msg_type(binary_string[:6])
    msg_values = message.call(msg_type, binary_string)
    return msg_values
