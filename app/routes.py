
from flask import render_template, flash, redirect, url_for,  request
from werkzeug.urls import url_parse

from app import app,dbr

from config import Config

from werkzeug.utils import secure_filename



@app.route('/', methods=['GET', 'POST'])
def welcome():

    polvertex = "[46.147919, 9.357],[46.1495, 9.351365],[46.1475, 9.345],[46.1455, 9.351365],[46.147,9.357730]"

    marker = [ {'coord':"[46.147919, 9.357]"   ,'icon':"flag",     'color':"green", 'spin':"false"},
               {'coord':"[46.136770,9.364749]" ,'icon':"home",     'color':"yellow",'spin':"false"},
               {'coord':"[46.1475,9.345]"      ,'icon':"arrow-up", 'color':"blue",  'spin':"false"},
               {'coord':"[46.147,9.35]"        ,'icon':"arrow-up", 'color':"blue",  'spin':"true"},
               {'coord':"[46.147,9.357730]"    ,'icon':"arrow-down",'color':"blue", 'spin':"false"}
             ]
               
     
    pagedat = {'title' : "Geas NBC buoy position",'polvertex':polvertex,'marker':marker}
        
    return render_template('index.html', pagedat=pagedat)

@app.route('/boa/<boa_id>', methods=['GET','POST'])
def update_boa_pos (boa_id):
    if request.method == 'POST':
        print ("boa_id",boa_id)
        content = request.json
        print (content,type(content),len(content))
        dbr.hmset (boa_id,content)
        return "wpost",200
    else:
        val =dbr.hgetall (boa_id)
        print (type(val),val)
        return "rget",200


@app.route('/boa', methods=['GET'])
def get_boa_dat ():
    s = ""
    for boa in dbr.keys():
         s = s + str(boa)
         print (boa)
         s = s + str(dbr.hgetall (boa))
    return s,200     

