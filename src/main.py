from typing import Union, List, Tuple
import message
from decode import decode_msg
from values import get_msg_type

def get_msg_parts(raw: str):
    return raw.split(",")


def preproc_multipart_msg(messages: Union[str, List[str]]) -> Tuple[str, int]:

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
    
def ais_decode(raw):
    if not raw:
        return f"Empty message: {raw}"
    
    payload, shift = preproc_multipart_msg(raw)
    binary_string = decode_msg(payload.encode(), shift)
    msg_type = get_msg_type(binary_string[:6])
    msg_values = message.call(msg_type, binary_string)
    return msg_values

if __name__ == "__main__":
    
    s1 = [
        [
            '!AIVDM,2,1,0,A,544tCa`00001D9USD0084LU8400000000000000010N33vD`N3BhDPEC880000,0*69',
            '!AIVDM,2,2,0,A,000000000>Ih,4*3D',
        ],
    '!AIVDM,1,1,,A,13aG`h0P000Htt<N0D0l4@T40000,0*7C'
    ]

    for raw in s1:
        print(ais_decode(raw))
