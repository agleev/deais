"""
#Type 24A: Static Data Report

type = bit_string[:6]
repeat = bit_string[5:8]
mmsi =  bit_string[8:38]

partno = bit_string[38:40]
shipname = bit_string[40:160]
spare = bit_string[160:]


"""