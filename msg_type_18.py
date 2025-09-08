"""
#Type 18: Standard Class B CS Position Report

type = bit_string[:6]
repeat = bit_string[5:8]
mmsi =  bit_string[8:38]

reserved = bit_string[38:46]
sog = bit_string[46:56]
accuracy = bit_string[56:57]
lon = bit_string[57:85]
lat = bit_string[85:112]
cog = bit_string[112:124]
heading = bit_string[124:133]

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

"""