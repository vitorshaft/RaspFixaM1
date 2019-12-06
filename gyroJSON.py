import smbus			#import modulo SMBus do I2C
from time import sleep          #import sleep
import time
import os
import json
from gyroConfig import MPU_Init
from gyroConfig import read_raw_data as read_raw_data
from gyroConfig import ACCEL_XOUT_H as ACCEL_XOUT_H
from gyroConfig import ACCEL_YOUT_H as ACCEL_YOUT_H
from gyroConfig import ACCEL_ZOUT_H as ACCEL_ZOUT_H

dados = {}
dados['gyro'] = [0]

while True:
	try:
		
		#Read Accelerometer raw value
		acc_x = read_raw_data(ACCEL_XOUT_H)
		acc_y = read_raw_data(ACCEL_YOUT_H)
		acc_z = read_raw_data(ACCEL_ZOUT_H)
		
		#Full scale range +/- 250 degree/C as per sensitivity scale factor
		Ax = acc_x/16384.0
		Ay = acc_y/16384.0
		Az = acc_z/16384.0
		
		tempo = time.localtime()
		data = str(tempo[0])+"-"+str(tempo[1])+"-"+str(tempo[2])
		hora = tempo[3]
		minuto = tempo[4]
		seg = tempo[5]
		
		dados['gyro'][0] = {
		'date': data,
		'hora':hora,
		'minuto':minuto,
		'segundo':seg,
		'cosseno':Ax,
		'seno':Ay
		}
		print dados['gyro'][0]
		with open('gyroRT.json','w') as BD:
			json.dump(dados,BD)
		os.system('sudo cp gyroRT.json /home/pi/FTP')
		sleep(1)
	except:
		pass
