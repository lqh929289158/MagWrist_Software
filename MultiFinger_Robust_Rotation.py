import numpy as np
import serial
import signal
import sys
import time


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

def calibration_collection(ser):
	print("Ready to rotate your arm~")
	print("Press Ctrl+C")
	try:
		while 1:
			tmp = read_vector_from_serial(ser)
	except:
		B_list = []
		B=[]
		print("Collecting...(Press Ctrl+C to stop)")
	try:
		while 1:
			while B==[]:
				B = read_vector_from_serial(ser)
			B = B.flatten()
			B_list.append(B)
			B = []
	except:
		del B_list[-1]
		print("Calibration Complete!")
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

#match num (0~31) to binary code
#code[0]: if code[1~5] are all zeros, code[0] is 1, else is 0
#code[1~5]:index,middle,ring,little,thumb
def map_num_to_code(num):
	code = []
	for i in range(5):
		code.append(num>>i & 1)
	code = code[::-1]
	code.append(code[0])
	code[0] = 0
	if num==0:
		code[0]=1
	return code

#match code [x,x,x,x,x,x] to gesture name
#code[0]: NULL
#code[1~5]:"Index","Middle","Ring","Little","Thumb"
def map_code_to_name(code):
	finger_name_list = ["NULL","Index","Middle","Ring","Little","Thumb"]
	name = ""
	if code[5] == 1:
		name = name + finger_name_list[5]
	for i in range(len(code)-1):
		if code[i] == 1:
			if name != "":
				name = name+'+'
			name = name+finger_name_list[i]
	return name

#collect all gestures(32) data
#input: batch(num of vectors for each gesture)
#output: 3-D array with size (32,batch,dimension(30))
def multiple_finger_collection(ser,batch=40):

	original_signal = signal.getsignal(signal.SIGINT)

	print("Thank you for starting your contribution to data collection!")
	gesture_code_list = list(range(32))
	
	batch_list = []
	for i in gesture_code_list:
		code = map_num_to_code(i)
		name = map_code_to_name(code)
		print("\nStretch all fingers and keep steady.")
		print("Enter Ctrl+C.")

		#restore interrupt
		signal.signal(signal.SIGINT,original_signal)
		try:
			while 1:
				s = ser.readline()
		except:
			#disable interrupt! It is collecting data!
			signal.signal(signal.SIGINT,signal.SIG_IGN)
			B_null_finger = read_batch_from_serial(ser,batch=batch//5)
		print("\n\nBend "+name+" in Sequence.")
		print("Enter Ctrl+C.")

		#restore interrupt!
		signal.signal(signal.SIGINT,original_signal)

		try:
			while 1:
				s = ser.readline()
		except:
			#disable interrupt! It is collecting data!
			signal.signal(signal.SIGINT,signal.SIG_IGN)
			B_finger = read_batch_from_serial(ser,batch=batch)
		print(np.mean(B_finger,axis=0) - np.mean(B_null_finger,axis=0))

		batch_list.append(B_null_finger)
		batch_list.append(B_finger)
	posture_list = convert_batch_list_to_posture_list(batch_list)
	#remove null finger batch
	null_batch = posture_list[0]
	finger_list = posture_list[1:]
	return np.array(null_batch),np.array(finger_list)

#convert a batch list to difference vector list
#input: batch_list [null1_batch, finger1_batch,null2_batch,finger2_batch...]
#output: diff_list [null_batch_all, finger1_batch,finger2_batch...]
def convert_batch_list_to_diff_list(batch_list):
	for i in range(0,len(batch_list),2):
		base_vec = np.mean(batch_list[i],axis=0)
		#a batch of vector substract base vector
		batch_list[i] = batch_list[i]-base_vec
		batch_list[i+1] = batch_list[i+1]-base_vec
	null_list = [batch_list[i] for i in range(0,len(batch_list),2)]
	finger_list = [batch_list[i+1] for i in range(0,len(batch_list),2)]
	null_batch = np.vstack(null_list)
	return [null_batch]+finger_list

#convert a batch list to vector list for each posture
#input: batch_list [null1_batch, finger1_batch,null2_batch,finger2_batch...]
#output: diff_list [null_batch_all, finger1_batch,finger2_batch...]
def convert_batch_list_to_posture_list(batch_list):
	'''
	for i in range(0,len(batch_list),2):
		base_vec = np.mean(batch_list[i],axis=0)
		#a batch of vector substract base vector
		batch_list[i] = batch_list[i]-base_vec
		batch_list[i+1] = batch_list[i+1]-base_vec
	'''
	null_list = [batch_list[i] for i in range(0,len(batch_list),2)]
	finger_list = [batch_list[i+1] for i in range(0,len(batch_list),2)]
	null_batch = np.vstack(null_list)
	return [null_batch]+finger_list

np.set_printoptions(threshold=np.inf)
batch =20
loop_num=1


#argv[0] name of file
#argv[1...] arguments
volunteer = sys.argv[1]
position = sys.argv[2]
#print (sys.argv[0])

ser = serial.Serial('/dev/cu.usbmodem0F00577F',1500000)
calibration_data = calibration_collection(ser)

np.save(volunteer+"_"+position+"_calibration.npy",calibration_data)

# single finger gesture data collection
single_raw_vec_list = single_finger_collection(ser,batch)
single_diff_vec_list = convert_batch_list_to_posture_list(single_raw_vec_list)
single_diff_vec_array = np.array(single_diff_vec_list)

np.save(volunteer+"_"+position+"_"+"single.npy",single_diff_vec_array)

# multiple finger gesture data collection
multiple_null_vec_array,multiple_finger_vec_array = multiple_finger_collection(ser,batch)

np.save(volunteer+"_"+position+"_"+"null_multiple.npy",multiple_null_vec_array)
np.save(volunteer+"_"+position+"_"+"multiple.npy",multiple_finger_vec_array)

print("Thank you for your cooperation!")