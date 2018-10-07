import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import serial
import sys
import time
np.set_printoptions(threshold=np.inf)
from PCA_Display_Lib import *

#input:Serial object
#output:np.array[sensor_num][senor_dim]
def read_vector_from_serial(ser,sensor_num=10,sensor_dim=3):
	#sensor_dim = 3
	#sensor_num = 10
	B = np.empty((sensor_num,sensor_dim),np.int)
	#print("Reading Initial Vector...")
	
	cnt = 0
	cntlist = []
	while(cnt<10):
		s = ser.readline()
		s = s.decode()
		if(len(s) == 44):
			continue
		elif (len(s) == 23):
			s = s.split()
			idx = int(s[-1])
			if(idx in cntlist):
				continue
			else:
				cntlist.append(idx)
				cnt += 1
				if(int(s[0])==int(s[1]) and int(s[1])==int(s[2])):
					if(int(s[0])==1028):
						print("Some Sensor Crashed!!!!!!!!!!!!!!!!!!")
						return []
				for j in range(sensor_dim):
					if(abs(int(s[j]))>2047):
						print("WARNING!!!!!!!!!")
						return []
					elif(int(s[j])==1028):
						print("WARNING!!!!!!!!!")

					B[idx][j] = int(s[j])

		else:
			print("String Error")
			return []
	return B

def read_batch_from_serial(ser,batch=40,sensor_num=10,sensor_dim=3):
	B_list = []
	B=[]
	for i in range(batch):
		while B==[]:
			B = read_vector_from_serial(ser,sensor_num,sensor_dim)
		B = B.flatten()
		B_list.append(B)
		B = []
	return np.array(B_list)

def single_finger_collection(ser,batch=40):

	original_signal = signal.getsignal(signal.SIGINT)

	print("\nReady?Stretch all fingers and keep steady.")
	print("Enter Ctrl+C.")
	#restore interrupt
	signal.signal(signal.SIGINT,original_signal)
	try:
		while 1:
			s = ser.readline()
	except:
		signal.signal(signal.SIGINT,signal.SIG_IGN)
		B_null_index = read_batch_from_serial(ser,batch=batch//5)		
	print("\n\nBend your INDEX finger.")
	print("Enter Ctrl+C.")
	#restore interrupt
	signal.signal(signal.SIGINT,original_signal)
	try:
		while 1:
			s = ser.readline()
	except:
		signal.signal(signal.SIGINT,signal.SIG_IGN)
		B_index = read_batch_from_serial(ser,batch=batch)
	print(np.mean(B_index,axis=0) - np.mean(B_null_index,axis=0))

	print("\nStretch all fingers and keep steady.")
	print("Enter Ctrl+C.")
	#restore interrupt
	signal.signal(signal.SIGINT,original_signal)
	try:
		while 1:
			s = ser.readline()
	except:
		signal.signal(signal.SIGINT,signal.SIG_IGN)
		B_null_middle = read_batch_from_serial(ser,batch=batch//5)
	print("\n\nBend your MIDDLE finger.")
	print("Enter Ctrl+C.")
	#restore interrupt
	signal.signal(signal.SIGINT,original_signal)
	try:
		while 1:
			s = ser.readline()
	except:
		signal.signal(signal.SIGINT,signal.SIG_IGN)
		B_middle = read_batch_from_serial(ser,batch=batch)
	print(np.mean(B_middle,axis=0) - np.mean(B_null_middle,axis=0))

	print("\nStretch all fingers and keep steady.")
	print("Enter Ctrl+C.")
	#restore interrupt
	signal.signal(signal.SIGINT,original_signal)
	try:
		while 1:
			s = ser.readline()
	except:
		signal.signal(signal.SIGINT,signal.SIG_IGN)
		B_null_ring = read_batch_from_serial(ser,batch=batch//5)
	print("\n\nBend your Ring finger.")
	print("Enter Ctrl+C.")
	#restore interrupt
	signal.signal(signal.SIGINT,original_signal)
	try:
		while 1:
			s = ser.readline()
	except:
		signal.signal(signal.SIGINT,signal.SIG_IGN)
		B_ring = read_batch_from_serial(ser,batch=batch)
	print(np.mean(B_ring,axis=0) - np.mean(B_null_ring,axis=0))

	print("\nStretch all fingers and keep steady.")
	print("Enter Ctrl+C.")
	#restore interrupt
	signal.signal(signal.SIGINT,original_signal)
	try:
		while 1:
			s = ser.readline()
	except:
		signal.signal(signal.SIGINT,signal.SIG_IGN)
		B_null_little = read_batch_from_serial(ser,batch=batch//5)
	print("\n\nBend your Little finger.")
	print("Enter Ctrl+C.")
	#restore interrupt
	signal.signal(signal.SIGINT,original_signal)
	try:
		while 1:
			s = ser.readline()
	except:
		signal.signal(signal.SIGINT,signal.SIG_IGN)
		B_little = read_batch_from_serial(ser,batch=batch)
	print(np.mean(B_little,axis=0) - np.mean(B_null_little,axis=0))

	print("\nStretch all fingers and keep steady.")
	print("Enter Ctrl+C.")
	#restore interrupt
	signal.signal(signal.SIGINT,original_signal)
	try:
		while 1:
			s = ser.readline()
	except:
		signal.signal(signal.SIGINT,signal.SIG_IGN)
		B_null_thumb = read_batch_from_serial(ser,batch=batch//5)
	print("\n\nBend your Thumb finger.")
	print("Enter Ctrl+C.")
	#restore interrupt
	signal.signal(signal.SIGINT,original_signal)
	try:
		while 1:
			s = ser.readline()
	except:
		signal.signal(signal.SIGINT,signal.SIG_IGN)
		B_thumb = read_batch_from_serial(ser,batch=batch)
	print(np.mean(B_thumb,axis=0) - np.mean(B_null_thumb,axis=0))

	print("Collection Finished!")
	signal.signal(signal.SIGINT,original_signal)
	return [B_null_index,B_index,\
			B_null_middle,B_middle,\
			B_null_ring,B_ring,\
			B_null_little,B_little,\
			B_null_thumb,B_thumb]

def many_interactive_collection(ser,batch,loop):
	pos_list = []
	for i in range(loop):
		batch_list = single_finger_collection(ser,batch)
		pos_list.append(batch_list)
		print("Move magnets or Change your posture.")
	print("Data Collection Completed!Please wait for training")
	return pos_list

def convert_from_batch_to_vector(pos_list):
	res_list = []
	for i in range(len(pos_list)):
		finger_array = []
		for j in range(5):
			#finger vector mean - null vector mean
			finger_array.append(np.mean(pos_list[i][2*j+1],axis=0)-np.mean(pos_list[i][2*j],axis=0))
		res_list.append(np.array(finger_array))
	return res_list

def save_vectors_to_file(pos_list,f,row_num,col_num):
	pos_num = len(pos_list)

	#f.write(str(pos_num)+'\n')
	f.write(str(row_num)+' '+str(col_num)+'\n')
	for i in range(pos_num):
		for j in range(5):
			for k in range(len(pos_list[i][j])):
				f.write(str(pos_list[i][j][k])+'\t')
			f.write('\n')
		f.write('\n')



batch = 5
row_num = 4
col_num = 9
loop_num = row_num*col_num

ser = serial.Serial('/dev/cu.usbmodem0F005B71',1500000)

pos_list = many_interactive_collection(ser,batch,loop_num)
pos_list = convert_from_batch_to_vector(pos_list)


volunteer = sys.argv[1]

f = open('finger_vectors_file_'+volunteer+'.txt','w')
save_vectors_to_file(pos_list,f,row_num,col_num)



