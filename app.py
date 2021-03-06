from flask import Flask, jsonify, request
from flask_cors import CORS
from astropy import units as u
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time, TimeDelta
import pandas as pd
import datetime
import pytz
import glob
import os

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

#CWD (this should probably change)
basedir=os.getcwd()

#Target list
defs=pd.read_csv("public/assets/introtargets.csv")
mess=pd.read_csv("public/assets/messierobjects.csv")

#Locations
locations={
    'mrc' : EarthLocation(lat=34, lon=-120, height=390*u.m),
    'saf' : EarthLocation(lat=36, lon=-106, height=390*u.m),
    'coj' : EarthLocation(lat=-31, lon=149, height=1116*u.m),
    'cpt' : EarthLocation(lat=-32, lon=20, height=1760*u.m),
    'tfn' : EarthLocation(lat=28, lon=-16, height=2330*u.m),
    'lsc' : EarthLocation(lat=-30, lon=-70, height=2198*u.m),
    'elp' : EarthLocation(lat=30, lon=-104, height=2070*u.m),
    'ogg' : EarthLocation(lat=20, lon=-156, height=3055*u.m),
    'tlv' : EarthLocation(lat=30, lon=34, height=875*u.m)
}

#Timezones
tzs={
    'mrc' : 'US/Pacific',
    'saf' : 'US/Mountain',
    'coj' : 'Australia/Sydney',
    'cpt' : 'Africa/Johannesburg',
    'tfn' : 'Atlantic/Canary',
    'lsc' : 'America/Santiago',
    'elp' : 'US/Central',
    'ogg' : 'US/Hawaii',
    'tlv' : 'Israel'
}

# form entry and response
@app.route('/ping', methods=['POST','GET'])
def defsearch():
    post_data = request.get_json()
    location1=post_data.get('location1')
    lat1=post_data.get('lat1')
    lon1=post_data.get('lon1')
    dateobs=post_data.get('dateobs')
    timeobs=post_data.get('timeobs')
    tzinfo=post_data.get('tzinfo')
    offset=post_data.get('offset')                              #user's UTC offset in min
    messier=post_data.get('messier')
  
    if location1 == "0" and len(lat1)>0 and len(lon1)>0:        #use lat/long if not at PTR
        locn=EarthLocation.from_geodetic(lat=lat1, lon=lon1, height=390*u.m)
    else:
       locn=locations[location1]

    #Set UTC offset based on time entry method
    if tzinfo == "my":
        utcoffset=offset
    elif tzinfo == "lcl":
        utcoffset=datetime.datetime.now(pytz.timezone(tzs[location1])).utcoffset().total_seconds()/60
    elif tzinfo == "utc":
        utcoffset=0

    start=Time(dateobs+'T'+timeobs)                             #in student's local time 

    starttime=Time(start)+utcoffset*u.min                       #start time in UTC
    endtime=starttime+TimeDelta(1800.0, format='sec')           #end time if block is 30min

    #Find list of targets
    diclist=[]

    if messier=='yes':
        targs=mess
    else:
        targs=defs

    #Retrieve alt/az for each target at start and end of observing time
    for i in range(len(targs["Object Name"])):
        target=targs["Object Name"][i]
        coordstart = SkyCoord.from_name(target).transform_to(AltAz(obstime=starttime,location=locn))
        coordend = SkyCoord.from_name(target).transform_to(AltAz(obstime=endtime,location=locn))
        minalt = SkyCoord(0*u.deg, 35*u.deg, frame='altaz')     #minimum altitude
        zero = SkyCoord(0*u.deg, 0*u.deg, frame='altaz')        #zero altitude
     
    #Sort through for targets above minimum altitude
        if coordstart.alt-minalt.alt > zero.alt and coordend.alt-minalt.alt > zero.alt:
            os.chdir(basedir+'/public/assets/DefaultTargetImages')
            image='/assets/DefaultTargetImages/'+glob.glob(target.replace(" ", "")+"_*")[0]
            diclist.append({"name": target, 'type': targs['Group'][i], 'image': image})
         
    os.chdir(basedir)
    
    return jsonify(diclist)

if __name__ == '__main__':
    app.run()