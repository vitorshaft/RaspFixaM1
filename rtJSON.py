#import smbus			#import modulo SMBus do I2C
from time import sleep          #import sleep
import time
import os
import json
import math
import serial

dados = {}
dados['realTime'] = [0]
log = {}
log['Log'] = {}

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1) #Arduino Uno
Nano = serial.Serial('/dev/ttyUSB0',9600, timeout=1) #Arduino Nano

def txBase():
	ser.write('t')

def rxSat():
	chave = True
	while a == True:
		if Nano.in_waiting > 0:
			linha = Nano.readline().decode('utf-8').rstrip()
			chave = False
			#txBase()
			return linha
		

while True:
	try:
		Ax = 1.1
		Ay = 1.1
		Az = 1.1
		
		sat = rxSat()
		mensagem = []
		mensagem = sat.split(";")
		end = mensagem[2]
		
		tempo = time.localtime()
		data = str(tempo[0])+"-"+str(tempo[1])+"-"+str(tempo[2])
		hora = tempo[3]
		minuto = tempo[4]
		seg = tempo[5]
		XYZ = 'xx.xxxx,yy.yyyy,zz.zzzz'
		xyz = 'x,y,z'
		DTG = 'aaaa-mm-dd-hh-mm-ss'
		if end == 15:
			rx = mensagem[0]
			RX = rx.split(",")
			DTGsat = RX[2]
			posSat = RX[1]
			nPkgSat = mensagem[3]
			nPKG = nPkgSat
			rs = mensagem[1]
			log['Log'][nPKG] = {
			'pkg': nPKG,	# num pacote recebido por ultimo, ID de quem recebeu o pkg
			'dtg': (data,hora,minuto,seg),
			'AzElPo':(Ax,Ay,Az),
			'LatLongBase':(XYZ),
			'posSat':(XYZ),
			'dtgTX':DTG,
			'dtgTele':DTG,
			'RSSI':rs
			}
			txBase()
		
		elif end == 1:
			rx = mensagem[0]
			RX = rx.split(",")
			DTG1 = RX[2]
			posSat1 = RX[1]
			XYZ1 = RX[0]
			nPkgB1 = mensagem[3]
			nPKG = nPkgB1
			rs = mensagem[1]
			log['log'][nPKG]['Base1'] = {'posBase':(XYZ1),'dtgBase':(DTG1), 'posSat':(posSat1)}
			
			
			
		elif end == 2:
			rx = mensagem[0]
			RX = rx.split(",")
			DTG2 = RX[2]
			posSat2 = RX[1]
			XYZ2 = RX[0]
			nPkgB2 = mensagem[3]
			nPKG = nPkgB2
			rs = mensagem[1]
			log['log'][nPKG]['Base2'] = {'posBase':(XYZ2),'dtgBase':(DTG2), 'posSat':(posSat2)},
		
		elif end == 3:
			rx = mensagem[0]
			RX = rx.split(",")
			DTG3 = RX[2]
			posSat3 = RX[1]
			XYZ3 = RX[0]
			nPkgB3 = mensagem[3]
			nPKG = nPkgB3
			rs = mensagem[1]
			log['log'][nPKG]['Base3'] = {'posBase':(XYZ3),'dtgBase':(DTG3), 'posSat':(posSat3)}
			
		else:
			pass
			
		
		dados['realTime'][0] = {}
		print dados['realTime'][0]
		with open('RT.json','w') as BD:
			json.dump(dados,BD)
		BD.close()
		with open('Log.json','w') as LG:
			json.dump(log,LG)
		LG.close()
		os.system('sudo cp RT.json /home/pi/FTP')
		os.system('sudo cp Log.json /home/pi/FTP')
		time.sleep(1)
	except:
		break
		#criar tecla de saida do script

