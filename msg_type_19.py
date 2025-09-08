"""
Type 19: Extended Class B CS Position Report

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
regional = bit_string[139:143]
shipname = bit_string[143:263]
shiptype = bit_string[263:271]

to_bow = bit_string[271:280]
to_stern = bit_string[280:289]
to_port = bit_string[289:295]
to_starboard = bit_string[295:301]

epfd = bit_string[301:305]
raim = bit_string[305:306]
dte = bit_string[306:307]
assigned = bit_string[307:308]
spare = bit_string[308:]
"""