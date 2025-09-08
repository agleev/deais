
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