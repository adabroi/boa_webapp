
from flask import render_template, flash, redirect, url_for,  request
from werkzeug.urls import url_parse

from app import app,dbr

from config import Config

from werkzeug.utils import secure_filename
import re

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

    if "role" in in_data:
        result = re.match (role_pattern,in_data["role"])
        if result:
            markdata["role"] = result.group(0)

    return (markdata)

def marker_add_entry (marker,boa_id,coord,icon,color,spin,popup,boa_role=""):
    if coord in marker:
        # already exist
        marker[coord]['popup'] += f' <br> {popup} - boa {boa_id}'
    else:
        marker[coord] = {'coord':coord,'icon':icon,'color':color,'spin':spin,'popup':f'{popup} - boa {boa_id}({boa_role})'}    

    print (marker.keys())

def get_markers ():
    marker = {}

    for boa in dbr.keys():

        boa_id = boa.decode("utf-8")
        val = dbr.hgetall (boa)
    
        if b'role' in val:
            role_name = val[b'role'].decode("utf-8")
        else:
            role_name = ""

        if b'home' in val:
            marker_add_entry (marker,boa_id,val[b'home'].decode("utf-8"),"home","yellow","false",'home',role_name)

        if b'rc' in val:
            marker_add_entry (marker,boa_id,val[b'rc'].decode("utf-8"),"flag","green","false",'rc',role_name)

        if b'target' in val:
            marker_add_entry (marker,boa_id,val[b'target'].decode("utf-8"),"arrow-up","blue","false",'target',role_name)

        if b'current' in val:
            marker_add_entry (marker,boa_id,val[b'current'].decode("utf-8"),"arrow-up","blue","true",'current',role_name)
        

    
    return marker.values()    

@app.route('/', methods=['GET', 'POST'])
def welcome():

    #polvertex = "[46.147919, 9.357],[46.1495, 9.351365],[46.1475, 9.345],[46.1455, 9.351365],[46.147,9.357730]"

    #marker = [ {'coord':"[46.147919, 9.357]"   ,'icon':"flag",     'color':"green", 'spin':"false"},
    #           {'coord':"[46.136770,9.364749]" ,'icon':"home",     'color':"yellow",'spin':"false"},
    #           {'coord':"[46.1475,9.345]"      ,'icon':"arrow-up", 'color':"blue",  'spin':"false"},
    #           {'coord':"[46.147,9.35]"        ,'icon':"arrow-up", 'color':"blue",  'spin':"true"},
    #           {'coord':"[46.147,9.357730]"    ,'icon':"arrow-down",'color':"blue", 'spin':"false"}
    #         ]
               
    marker = get_markers()
    pagedat = {'title' : "Geas NBC buoy position",'marker':marker}
        
    return render_template('index.html', pagedat=pagedat)

@app.route('/boa/<boa_id>', methods=['GET','POST'])
def update_boa_pos (boa_id):
    if request.method == 'POST':
        print ("boa_id",boa_id)
        content = request.json
        print (content,type(content),len(content))

        content_filtered = filter_input_data (content)
        if len(content_filtered) == 0:
            return "data not valid",404

        dbr.hmset (boa_id,content_filtered)
        dbr.expire (boa_id,60)
        return "ok",200
    else:
        val =dbr.hgetall (boa_id)
        print (type(val),val)
        return "rget",200


@app.route('/boa', methods=['GET'])
def get_boa_dat ():
    s = "boa_data --->"
    for boa in dbr.keys():
         s = s + str(boa)
         print (boa)
         s = s + str(dbr.hgetall (boa))
    s = s + "<---"
    return s,200     

