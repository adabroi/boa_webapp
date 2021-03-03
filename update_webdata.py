import json
import requests
import re

data_b = {"role"   : "bolina","home"    : "[46.136770,9.364749]","rc"      : "[46.147919,9.357]","target"  :"[46.1475,9.345]","current" :"[46.147,9.35]"}
data_s = {"role"   : "stacchetto","home"    : "[46.136770,9.364749]","rc"      : "[46.147919,9.357]","target"  :"[46.15,9.345]","current" :"[46.14,9.36]"}


def update_map_data (data,boa_id):

    response = requests.post(f'http://127.0.0.1:5000/boa/{boa_id}', json=data)
    return response.status_code


#ret = update_map_data (data)
#print (ret)

def filter_input_data (in_data):
    coord_pattern = "^\[(?P<nord>[+-]?([0-9]*[.])?[0-9]+),(?P<est>[+-]?([0-9]*[.])?[0-9]+)\]$"
    role_pattern  = "^(?P<rolname>\w+)$"

    expected_coord = ["home","rc","target","current"]

    markdata = {}

    for key in expected_coord:
         if key in in_data:
            result = re.match(coord_pattern, in_data[key])
            if result:
                markdata[key] = result.group(0)

    if len (markdata) == 0:
        return {}

    if "role" in data:
        result = re.match (role_pattern,in_data["role"])
        if result:
            markdata["role"] = result.group(0)

    return (markdata)

#print (filter_input_data(data))
print (update_map_data (data_b,1))
print (update_map_data (data_s,2))