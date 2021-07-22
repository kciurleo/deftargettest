from flask import Flask, jsonify, request
from flask_cors import CORS
from astropy import units as u
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time, TimeDelta
import pandas as pd
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
targs=pd.read_csv("public/assets/introtargets.csv")

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
    'tlv ': EarthLocation(lat=30, lon=34, height=875*u.m)
}

# form entry and response
@app.route('/ping', methods=['POST','GET'])
def defsearch():
    '''
    location1='mrc'
    lat1='0'
    lon1='0'
    
    dateobs='2020-07-07'
    timeobs='22:00:00'
    timezone='-7:00'
    offset=0
    '''
    post_data = request.get_json()
    location1=post_data.get('location1')
    lat1=post_data.get('lat1')
    lon1=post_data.get('lon1')
    dateobs=post_data.get('dateobs')
    timeobs=post_data.get('timeobs')
    tzinfo=post_data.get('tzinfo')
    offset=post_data.get('offset')                              #user's UTC offset in min
    #'''
    if location1 == "0" and len(lat1)>0 and len(lon1)>0:        #use lat/long if not at PTR
        locn=EarthLocation.from_geodetic(lat=lat1, lon=lon1, height=390*u.m)
    elif location1 == "0":
        return("Please input your location or latitude and longitude.")
    else:
       locn=locations[location1]

    start=Time(dateobs+'T'+timeobs)

    if tzinfo == "my":                                          #option for student's time or UTC
        utcoffset=offset
    #else if tzinfo = "local":
        #utcoffset=?
    else if tzinfo == "utc":
        utcoffset=0

    starttime=Time(start)-utcoffset*u.min                          #start time in UTC
    endtime=starttime+TimeDelta(1800.0, format='sec')           #end time if block is 30min
    #return(str(locn) +' \n' + str(start) +' \n' + str(starttime) +' \n' +str(endtime) +' \n' )

    #Start with default targets
    diclist=[]
    
    #Retrieve alt/az for each target at start and end of observing time
    for i in range(len(targs["Object Name"])):
        target=targs["Object Name"][i]
        coordstart = SkyCoord.from_name(target).transform_to(AltAz(obstime=starttime,location=locn))
        coordend = SkyCoord.from_name(target).transform_to(AltAz(obstime=endtime,location=locn))
        minalt = SkyCoord(0*u.deg, 45*u.deg, frame='altaz')     #minimum altitude
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