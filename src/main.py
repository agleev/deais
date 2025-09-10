
from .decode import decode_msg

def preproc_msg(raw: str):
    return raw.split(",")
    

def main_msg_decode(raw_data):
    
    for raw in raw_data:
        (package_name,
         count_frags,
         num_frags,
         _,
         ab_code,
         payload,
         shift,
         checksum) = preproc_msg(raw)
        
        binary_string = decode_msg(payload.encode('utf-8'))