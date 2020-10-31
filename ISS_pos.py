import pyproj
#import orbit-predictor
from orbit_predictor.sources import EtcTLESource
#from orbit_predictor.locations import brazil
from orbit_predictor.sources import get_predictor_from_tle_lines
import datetime
from datetime import datetime

TLE_LINES = (
    "1 25544U 98067A   20292.96180177  .00000594  00000-0  18740-4 0  9996",
    "2 25544  51.6435  96.0270 0001354  46.8738  91.3465 15.49312758251202")

now = datetime.now()
'''
ano,mes,dia = now.strftime("%Y"),now.strftime("%m"),now.strftime("%d")
h,m,s = now.strftime("%H"),now.strftime("%M"),now.strftime("%S")
'''
predictor = get_predictor_from_tle_lines(TLE_LINES)
pre = predictor.get_position(now)

x = pre[1][0]
y = pre[1][1]
z = pre[1][2]

ecef = pyproj.Proj(proj='geocent',ellps='WGS84',datum='WGS84')
lla = pyproj.Proj(proj='latlong',ellps='WGS84',datum='WGS84')
lon, lat, alt = pyproj.transform(ecef,lla,x,y,z,radians=False)

print(lat,lon,alt)
