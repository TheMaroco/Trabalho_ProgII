# module GPXparser

""" Parser used to initialize a GPXDocument object """

from xml.dom.minidom import parse
import datetime
import re

import myPyGPX  # avoids circular imports

# GPX date format(s) used for parsing. The T between date and time and Z after
# time are allowed, too:
DATE_FORMATS = [
    '%Y-%m-%d %H:%M:%S',
    '%Y-%m-%d %H:%M:%S.%f'
]

def parseTime(string):	
    """ Parses the date formatted as string

    Requires:
      a string that represents the date and time in the format
      AAAA-MM-DDTHH:MM:SS.MSZ (optional T and Z),
      or an empty string
    Ensures:
      a native object of type datetime containing the parcels of time:
      (year, month, day, hour, minute, second, milisecond)
    """	
     
    if string == "":
        result = None
    if 'T' in string:
        string = string.replace('T', ' ')
    if 'Z' in string:
        string = string.replace('Z', '')    

    if len(string) < 19:
        # string has some single digits
        p = """^([0-9]{4})-([0-9]{1,2})-([0-9]{1,2}) 
        ([0-9]{1,2}):([0-9]{1,2}):([0-9]{1,2}).*$"""
        s = re.findall(p, string)
        if len(s) > 0:
            string = '{0}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}'\
                .format(*[int(x) for x in s[0]])

    for date_format in DATE_FORMATS:
        try:
            result = datetime.datetime.strptime(string, date_format)
        except ValueError:
            pass

    return result
			
def parsePoint(point):
    """ Parses any type of point (trkpt, rtept and wpt) from the DOM model

    Requires:
      point is a GPX element of any type of the points mentioned
    Ensures:
      a tuple of values extracted from the point that include
      (latitude, longitude, time, elevation, name and description)
    """        
    lat = float(point.getAttribute("lat"))
    lon = float(point.getAttribute("lon"))
    name = ""
    for e in point.getElementsByTagName("name"):
        name = e.childNodes[0].data.strip()
    description = ""   
    for e in point.getElementsByTagName("description"):
        description = e.childNodes[0].data.strip()            
    ele = 0
    for e in point.getElementsByTagName("ele"):
        ele = float(e.childNodes[0].data.strip())
    t = None
    time = None
    for e in point.getElementsByTagName("time"):
        t = parseTime(e.childNodes[0].data.strip())
        secMil = t.second + t.microsecond / 1000000
        time = myPyGPX.Time(t.year, t.month, t.day, t.hour, t.minute, secMil)
    return (lat,lon, time, ele, name, description)

def buildTrack(trk):
    """ Processes a trk from the DOM model and returns a Track object.
    
    Requires:
      a structure containing the track (trk) extracted from the DOM model
    Ensures:
      a Track object containing a list of TrackSeg filled with TrackPoint
    """
    track = myPyGPX.Track()       
    for trkseg in trk.getElementsByTagName("trkseg"):
        ts = myPyGPX.TrackSeg()
        for trkpt in trkseg.getElementsByTagName("trkpt"):
            (lat, lon, t, ele, name, description) = parsePoint(trkpt)
            ts.addPoint(myPyGPX.TrackPoint(lat,lon, t, ele))
        track.addTrackSeg(ts)
    return track

def buildRoute(rte):
    """ Processes a rte from the DOM model and returns a Route object.
    
    Requires:
      a structure containing the route (rte) extracted from the DOM model
    Ensures:
      a Route object with all the route points (RoutePoint)
    """
    route = myPyGPX.Route()
    for rtept in rte.getElementsByTagName("rtept"):
        (lat,lon, t, ele, name, description) = parsePoint(rtept)
        route.addPoint(myPyGPX.RoutePoint(lat, lon, ele, name, description))        
    return route
	
def buildWayPointList(dom):
    """ Processes the DOM model and returns a WayPoint list.
    
    Requires:
      a DOM model
    Ensures:
      a list of waypoints (WayPoint)
    """
    waypoints =  []
    for wpt in dom.getElementsByTagName("wpt"):
        (lat,lon, t, ele, name, description) = parsePoint(wpt)
        waypoints.append(myPyGPX.WayPoint(lat, lon, ele, name, description))
    return waypoints
    
def buildGPXDocument(gpxFileName, someGPXDocument):
    """ Initializes a GPXDocument object from a GPX file
    
    Requires:
      gpxFileName is a string that names a reachable GPX file;
      this file contains at most 1 track;
      this file contains at most 1 route. 
    """
    # obtains the DOM representation of the GPX file
    # (the content of the file instantiated in a structure of xml.dom.minidom)
    dom = parse(gpxFileName)
    for trk in dom.getElementsByTagName("trk"):
        someGPXDocument.setTrack(buildTrack(trk))
    for rte in dom.getElementsByTagName("rte"):
        someGPXDocument.setRoute(buildRoute(rte))       
    someGPXDocument.setWayPoints(buildWayPointList(dom))
