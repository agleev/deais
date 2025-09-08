"""
#Type 4: Base Station Report
#Type 11: UTC/Date Response

type = bit_string[:6]
repeat = bit_string[5:8]
mmsi =  bit_string[8:38]

year = bit_string[38:52]
month = bit_string[52:56]
day = bit_string[56:61]
hour = bit_string[61:66]
minute = bit_string[66:72]
second = bit_string[72:78]

accuracy = bit_string[78:79]
lon = bit_string[79:107]
lat = bit_string[107:134]
epfd = bit_string[134:138]
spare = bit_string[138:148]
raim = bit_string[148:149]
radio = bit_string[149:]

"""