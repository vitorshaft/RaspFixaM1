#import smbus			#import modulo SMBus do I2C
from time import sleep          #import sleep
import time
import os
import json
import math
import serial
'''
from gyroConfig import MPU_Init
from gyroConfig import read_raw_data as read_raw_data
from gyroConfig import ACCEL_XOUT_H as ACCEL_XOUT_H
from gyroConfig import ACCEL_YOUT_H as ACCEL_YOUT_H
from gyroConfig import ACCEL_ZOUT_H as ACCEL_ZOUT_H
'''
dados = {}
dados['realTime'] = [0]
log = {}
log['Log'] = []

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1) #Arduino Uno
Nano = serial.Serial('/dev/ttyUSB0',9600, timeout=1) #Arduino Nano

def txBase():
	ser.write('t')

def rxSat():
	chave = True
	while a == True:
		if Nano.in_waiting > 0:
			linha = Nano.readline().decode('utf-8').rstrip()
			#chave = False
			#txBase()
			return linha
		

while True:
	try:
		'''
		#Read Accelerometer raw value
		acc_x = read_raw_data(ACCEL_XOUT_H)
		acc_y = read_raw_data(ACCEL_YOUT_H)
		acc_z = read_raw_data(ACCEL_ZOUT_H)
		
		#Full scale range +/- 250 degree/C as per sensitivity scale factor
		Ax = acc_x/16800.0
		Ay = acc_y/16400.0
		Az = acc_z/1680.0
		
		#Ax = acc_x/16384.0
		#Ay = acc_y/16384.0
		#Az = acc_z/16384.0
		
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
		'''
		Ax = 1.1
		Ay = 1.1
		Az = 1.1
		
		sat = rxSat()
		mensagem = []
		mensagem = sat.split(";")
		end = mensagem[2]
		if end == 15:
			rx = mensagem[0]
			RX = rx.split(",")
			DTGsat = RX[2]
			posSat = RX[1]
			nPKG = mensagem[3]
			rs = mensagem[1]
			
		
		elif end == 1:
			rx = mensagem[0]
			RX = rx.split(",")
			DTG1 = RX[2]
			posSat1 = RX[1]
			XYZ1 = RX[0]
			nPKG = mensagem[3]
			rs = mensagem[1]
			
		elif end == 2:
			rx = mensagem[0]
			RX = rx.split(",")
			DTG2 = RX[2]
			posSat2 = RX[1]
			XYZ2 = RX[0]
			nPKG = mensagem[3]
			rs = mensagem[1]
		
		elif end == 3:
			rx = mensagem[0]
			RX = rx.split(",")
			DTG3 = RX[2]
			posSat3 = RX[1]
			XYZ3 = RX[0]
			nPKG = mensagem[3]
			rs = mensagem[1]
			
		else:
			
			XYZ = 'xx.xxxx,yy.yyyy,zz.zzzz'
			xyz = 'x,y,z'
			DTG = 'aaaa-mm-dd-hh-mm-ss'
			DTG1 = DTG
			DTG2 = DTG
			DTG3 = DTG
			[posSat, posSat1,posSat2,posSat3] = [XYZ,XYZ,XYZ,XYZ]
			nPKG = 0
			rs = 0
			
		
		tempo = time.localtime()
		data = str(tempo[0])+"-"+str(tempo[1])+"-"+str(tempo[2])
		hora = tempo[3]
		minuto = tempo[4]
		seg = tempo[5]
		
		
		
		
		dados['realTime'][0] = {
		'dtg': (data,hora,minuto,seg),	#data-hora da Base Fixa
		'AzElPo':(Ax,Ay,Az),
		'LatLongBase':(XYZ),
		'posSat': posSat,
		'dtgTX':DTGsat,		#timestamp do Satelite
		'dtgTele':'DTG',
		'RSSI':rs,
		'Base1':{'posBase':(XYZ1),'dtgBase':(DTG1), 'posSat':(posSat1)},
		'Base2':{'posBase':(XYZ2),'dtgBase':(DTG2), 'posSat':(posSat2)},
		'Base3':{'posBase':(XYZ3),'dtgBase':(DTG3), 'posSat':(posSat3)},
		'pkgCount':nPKG
		}
		log['Log'].append({
		'dtg': (data,hora,minuto,seg),
		'AzElPo':(Ax,Ay,Az),
		'LatLongBase':(XYZ),
		'posSat':(XYZ),
		'dtgTX':DTG,
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

