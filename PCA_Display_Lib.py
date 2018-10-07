import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.decomposition import KernelPCA
from sklearn.tree import DecisionTreeClassifier
import scipy as sp
import serial
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
						print("Error!!!!!!!!!!!!!!!!!")
				for j in range(sensor_dim):
					if(abs(int(s[j]))>2047):
						print("WARNING!!!!!!!!!")
					elif(int(s[j])==1028):
						print("WARNING!!!!!!!!!")

					B[idx][j] = int(s[j])

		else:
			print("String Error")
			return []
	'''
	for i in range(sensor_num):
		s = ser.readline()
		s = s.decode()
		if(len(s)!= 23):
			print("String Error")
			return []
		s = s.split()
		idx = int(s[-1])
		for j in range(sensor_dim):
			B[idx][j] = int(s[j])
	'''
	return B

def read_batch_from_serial(ser,batch=40,sensor_num=10,sensor_dim=3):
	B_list = []
	B=[]
	for i in range(batch):
		while B==[]:
			#print("here")
			B = read_vector_from_serial(ser,sensor_num,sensor_dim)
		B = B.flatten()
		B_list.append(B)
		B = []
	return np.array(B_list)

def interactive_collection(ser,batch=40):

	print("Ready?Stretch all fingers and keep steady.")
	print("Enter Ctrl+C.")
	try:
		while 1:
			s = ser.readline()
	except:
		time_start = time.time()
		B_null_index = read_batch_from_serial(ser,batch=batch//5)
		time_end = time.time()
		print(time_end-time_start)
	print("Bend your INDEX finger.")
	print("Enter Ctrl+C.")
	try:
		while 1:
			s = ser.readline()
	except:
		B_index = read_batch_from_serial(ser,batch=batch)
	print(np.mean(B_index,axis=0) - np.mean(B_null_index,axis=0))

	print("Stretch all fingers and keep steady.")
	print("Enter Ctrl+C.")
	try:
		while 1:
			s = ser.readline()
	except:
		B_null_middle = read_batch_from_serial(ser,batch=batch//5)
	print("Bend your MIDDLE finger.")
	print("Enter Ctrl+C.")
	try:
		while 1:
			s = ser.readline()
	except:
		B_middle = read_batch_from_serial(ser,batch=batch)
	print(np.mean(B_middle,axis=0) - np.mean(B_null_middle,axis=0))

	print("Stretch all fingers and keep steady.")
	print("Enter Ctrl+C.")
	try:
		while 1:
			s = ser.readline()
	except:
		B_null_ring = read_batch_from_serial(ser,batch=batch//5)
	print("Bend your Ring finger.")
	print("Enter Ctrl+C.")
	try:
		while 1:
			s = ser.readline()
	except:
		B_ring = read_batch_from_serial(ser,batch=batch)
	print(np.mean(B_ring,axis=0) - np.mean(B_null_ring,axis=0))

	print("Stretch all fingers and keep steady.")
	print("Enter Ctrl+C.")
	try:
		while 1:
			s = ser.readline()
	except:
		B_null_little = read_batch_from_serial(ser,batch=batch//5)
	print("Bend your Little finger.")
	print("Enter Ctrl+C.")
	try:
		while 1:
			s = ser.readline()
	except:
		B_little = read_batch_from_serial(ser,batch=batch)
	print(np.mean(B_little,axis=0) - np.mean(B_null_little,axis=0))

	print("Stretch all fingers and keep steady.")
	print("Enter Ctrl+C.")
	try:
		while 1:
			s = ser.readline()
	except:
		B_null_thumb = read_batch_from_serial(ser,batch=batch//5)
	print("Bend your Thumb finger.")
	print("Enter Ctrl+C.")
	try:
		while 1:
			s = ser.readline()
	except:
		B_thumb = read_batch_from_serial(ser,batch=batch)
	print(np.mean(B_thumb,axis=0) - np.mean(B_null_thumb,axis=0))

	print("Collection Finished!")
	return [B_null_index,B_index,\
			B_null_middle,B_middle,\
			B_null_ring,B_ring,\
			B_null_little,B_little,\
			B_null_thumb,B_thumb]

def convert_batch_list_to_diff_list(batch_list):
	for i in range(0,len(batch_list),2):
		base_vec = np.mean(batch_list[i],axis=0)
		batch_list[i] = batch_list[i]-base_vec #a batch of vector substract base vector
		batch_list[i+1] = batch_list[i+1]-base_vec
	null_list = [batch_list[i] for i in range(0,len(batch_list),2)]
	finger_list = [batch_list[i+1] for i in range(0,len(batch_list),2)]
	null_batch = np.vstack(null_list)
	return [null_batch]+finger_list
def many_interactive_collection(ser,batch,loop):
	pos_list = []
	for i in range(loop):
		batch_list = interactive_collection(ser,batch)
		pos_list.append(batch_list)
		print("Move magnets or Change your posture.")
	print("Data Collection Completed!Please wait for training")
	return pos_list
	
def prepare_train_target_data(pos_list,choice="orignal"):
	#join vertically
	'''
	if choice == "difference":
		for j in range(len(pos_list)):
			base_vec = np.mean(pos_list[j][0],axis=0)
			for i in range(6):
				pos_list[j][i] = pos_list[j][i] - base_vec
	'''
	if choice == "difference":
		for j in range(len(pos_list)):#loop number
			for i in range(0,len(pos_list[j]),2):
				base_vec = np.mean(pos_list[j][i],axis=0)
				pos_list[j][i] = pos_list[j][i] - base_vec
				pos_list[j][i+1] = pos_list[j][i+1] - base_vec
	for j in range(len(pos_list)):
		#combine null together
		pos_list[j] = [np.vstack([pos_list[j][i] for i in range(0,10,2)])]+[pos_list[j][i] for i in range(1,10,2)]
	join_pos_list = [np.vstack([pos_list[j][i] for j in range(len(pos_list))]) for i in range(len(pos_list[0]))]
	train_data = np.vstack(join_pos_list)
	#print(train_data)
	target_data = []
	for i in range(len(join_pos_list)):
		target_data += [i]*len(join_pos_list[i])

	return train_data,np.array(target_data)

def classifier_train(train_data,target_data,classifier='svm'):
	if classifier == 'svm':
		clf = svm.SVC(gamma = 0.001, C = 100.)
	elif classifier == 'naive_bayes_gauss':
		clf = naive_bayes.GaussianNB()
	elif classifier == 'naive_bayes_multi':
		clf = naive_bayes.MultinomialNB()
	elif classifier == 'naive_bayes_bernu':
		clf = naive_bayes.BernoulliNB()
	elif classifier == 'linear_model_log':
		clf = linear_model.LogisticRegression(multi_class = 'ovr')
	elif classifier == 'gaussian_process_ovo':
		clf = gaussian_process.GaussianProcessClassifier(multi_class = 'one_vs_one')
	elif classifier == 'gaussian_process_ovr':
		clf = gaussian_process.GaussianProcessClassifier(multi_class = 'one_vs_rest')
	clf.fit(train_data,target_data)
	return clf