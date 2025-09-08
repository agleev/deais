"""
#Type 24B: Static Data Report

type = bit_string[:6]
repeat = bit_string[5:8]
mmsi =  bit_string[8:38]

partno = bit_string[38:40]

shiptype = bit_string[40:48]

vendorid = bit_string[48:66]
model = bit_string[66:70]
serial = bit_string[70:90]
callsign = bit_string[90:132]

to_bow = bit_string[132:141]
to_stern = bit_string[141:150]
to_port = bit_string[150:156]
to_starboard = bit_string[156:162]

spare = bit_string[162:]

"""