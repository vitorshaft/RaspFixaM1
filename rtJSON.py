import smbus			#import modulo SMBus do I2C
from time import sleep          #import sleep
import time
import os
import json
import math
from gyroConfig import MPU_Init
from gyroConfig import read_raw_data as read_raw_data
from gyroConfig import ACCEL_XOUT_H as ACCEL_XOUT_H
from gyroConfig import ACCEL_YOUT_H as ACCEL_YOUT_H
from gyroConfig import ACCEL_ZOUT_H as ACCEL_ZOUT_H

dados = {}
dados['realTime'] = [0]
log = {}
log['Log'] = []

while True:
	try:
		
		#Read Accelerometer raw value
		acc_x = read_raw_data(ACCEL_XOUT_H)
		acc_y = read_raw_data(ACCEL_YOUT_H)
		acc_z = read_raw_data(ACCEL_ZOUT_H)
		
		#Full scale range +/- 250 degree/C as per sensitivity scale factor
		Ax = acc_x/16800.0
		Ay = acc_y/16400.0
		Az = acc_z/1680.0
		'''
		Ax = acc_x/16384.0
		Ay = acc_y/16384.0
		Az = acc_z/16384.0
		'''
		if Ax > 1.0:
			Ax = 1.0
		elif Ax < -1.0:
			Ax = -1.0
		if Ay > 1.0:
			Ax = 1.0
		elif Ay < -1.0:
			Ax = -1.0
		
		Ax = math.degrees(math.asin(Ax))
		Ay = math.degrees(math.asin(Ay))
		
		tempo = time.localtime()
		data = str(tempo[0])+"-"+str(tempo[1])+"-"+str(tempo[2])
		hora = tempo[3]
		minuto = tempo[4]
		seg = tempo[5]
		XYZ = 'xx.xxxx,yy.yyyy,zz.zzzz'
		xyz = 'x,y,z'
		DTG = 'aaaa-mm-dd-hh-mm-ss'
		nPKG = 'xxxxxx'
		
		dados['realTime'][0] = {
		'dtg': (data,hora,minuto,seg),
		'AzElPo':(Ax,Ay,Az),
		'LatLongBase':(XYZ),
		'posSat':(XYZ),
		'dtgRX':DTG,
		'dtgTele':DTG,
		'RSSI':'xxx',
		'Base1':{'posBase':(XYZ),'dtgBase':(DTG), 'posSat':(XYZ)},
		'Base2':{'posBase':(XYZ),'dtgBase':(DTG), 'posSat':(XYZ)},
		'Base3':{'posBase':(XYZ),'dtgBase':(DTG), 'posSat':(XYZ)},
		'pkgCount':nPKG
		}
		log['Log'].append({
		'dtg': (data,hora,minuto,seg),
		'AzElPo':(Ax,Ay,Az),
		'LatLongBase':(XYZ),
		'posSat':(XYZ),
		'dtgRX':DTG,
		'dtgTele':DTG,
		'RSSI':'xxx',
		'Base1':{'posBase':(XYZ),'dtgBase':(DTG), 'posSat':(XYZ)},
		'Base2':{'posBase':(XYZ),'dtgBase':(DTG), 'posSat':(XYZ)},
		'Base3':{'posBase':(XYZ),'dtgBase':(DTG), 'posSat':(XYZ)},
		'pkgCount':nPKG
		})
		print dados['realTime'][0]
		with open('RT.json','w') as BD:
			json.dump(dados,BD)
		BD.close()
		with open('Log.json','w') as LG:
			json.dump(log,LG)
		LG.close()
		os.system('sudo cp RT.json /home/pi/FTP')
		time.sleep(1)
	except:
		break
		#criar tecla de saida do script

