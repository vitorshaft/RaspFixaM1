import requests
import time
import serial
ser = serial.Serial('COM3',9600)

satID = 25544
latAnt = -8.053889
longAnt = -34.881111
altAnt = 15
seg = 1

def azEl(ID,lat,long,alt,t):
    param = 'https://api.n2yo.com/rest/v1/satellite/positions/%d/%f/%f/%d/%d/&apiKey=558322-DZMU8M-2AW9TH-4KQS'%(ID,lat,long,alt,t)
    req = requests.get(param)
    rjson = req.json()
    az = rjson['positions'][0]['azimuth']
    el = rjson['positions'][0]['elevation']
    r = [az,el]

    return r

for item in range(60):
    pos = azEl(satID,latAnt,longAnt,altAnt,seg)
    print(pos)
    if(pos[1] > 0):
        ser.write(b'%d %d'%(int(pos[0]),-int(pos[1])))
    else:
        ser.write(b'%d'%(int(pos[0])))
    time.sleep(2)
    

ser.close()
    
