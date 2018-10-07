import numpy as np
from scipy import integrate
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.decomposition import KernelPCA
from sklearn.tree import DecisionTreeClassifier
import scipy as sp
import serial
import sys
import time
np.set_printoptions(threshold=np.inf)
batch =40
loop_num=4
from PCA_Display_Lib import *
'''
ser = serial.Serial('/dev/cu.usbmodem0F005B71',1500000)
print(ser)


pos_list=many_interactive_collection(ser,batch,loop_num)
train_data,target_data = prepare_train_target_data(pos_list,choice="difference")

np.savez('train_target_data_null_insert_4_4', train_data=train_data, target_data=target_data)
'''
npzfile = np.load('train_target_data_null_insert_4_4.npz')

train_data = npzfile['train_data']
target_data = npzfile['target_data']

finger_stat = []
for i in range(6):
	finger_stat.append([])#null,index,middle,ring,little,thumb
for i in range(6):#sensor num*dim
	for j in range(30):
		finger_stat[i].append([0,0,0])#[#-1,#0,#1]

z_thres=15
for i in range(len(train_data)):
	for j in range(30):
		if train_data[i][j]>z_thres:
			finger_stat[target_data[i]][j][2]+=1
		elif train_data[i][j]<-z_thres:
			finger_stat[target_data[i]][j][0]+=1
		else:
			finger_stat[target_data[i]][j][1]+=1

sign_cnt_thres = batch*loop_num//10*7
for i in range(6):
	for j in range(30):
		if finger_stat[i][j][0]>sign_cnt_thres:
			finger_stat[i][j]='-'
			continue
		elif finger_stat[i][j][1]>sign_cnt_thres:
			finger_stat[i][j]='0'
			continue
		elif finger_stat[i][j][2]>sign_cnt_thres:
			finger_stat[i][j]='+'
			continue
		else:
			finger_stat[i][j]='x'

#target_data = np.sign(target_data)
#pca = PCA(n_components = 'mle',svd_solver = 'full')
pca = PCA(n_components = 2,svd_solver = 'full')
compressed_data = pca.fit_transform(train_data)
print(pca.explained_variance_ratio_)
components_num = len(pca.explained_variance_ratio_)
'''
if (components_num>3):
	compressed_data = compressed_data[:,:2]
'''
fig = plt.figure(1)
axes = fig.add_subplot(111)

#Regularization for each dimension
compressed_data = compressed_data.astype(float)
for i in range(components_num):
	compressed_data[:,i] = compressed_data[:,i] / max([abs(compressed_data[:,i].max()),abs(compressed_data[:,i].min())])

clf = DecisionTreeClassifier().fit(compressed_data, target_data)
#clf = DecisionTreeClassifier().fit(train_data, target_data)
plot_step = 0.01

pca2 = PCA(n_components = 2,svd_solver = 'full')
pca2.fit(compressed_data)
x_min, x_max = compressed_data[:, 0].min() - 1, compressed_data[:, 0].max() + 1
y_min, y_max = compressed_data[:, 1].min() - 1, compressed_data[:, 1].max() + 1
xmesh, ymesh = np.meshgrid(np.arange(x_min,x_max,plot_step),np.arange(x_min,x_max,plot_step))

#zmesh = clf.predict(pca2.inverse_transform(np.c_[xmesh.ravel(), ymesh.ravel()]))
zmesh = clf.predict(np.c_[xmesh.ravel(), ymesh.ravel()])
#zmesh = clf.predict(ravel_array)

zmesh = zmesh.reshape(xmesh.shape)
cs = axes.contourf(xmesh, ymesh, zmesh,cmap=plt.cm.Set1)

'''
arange_list = [np.arange(-1,1,0.01)]*components_num
mesh_list = np.meshgrid(*arange_list)
ravel_array = np.array([item.ravel() for item in mesh_list]) #16*points
ravel_array = ravel_array.T #points * 16

zmesh = clf.predict(ravel_array)
pca2 = PCA(n_components = 2,svd_solver = 'full')
pca2.fit(compressed_data)
compressed_ravel_array = pca2.transform(ravel_array)
x = compressed_ravel_array[:,0]
y = compressed_ravel_array[:,1]

xi = np.linspace(x.min(),x.max(),1000)
yi = np.linspace(y.min(),y.max(),1000)

zi = griddata((x,y),zmesh,(xi[None,:],yi[:,None]),method='cubic')

cs = axes.contourf(xi, yi, zi,cmap=plt.cm.Set1)
'''
color_array = ['w','r','b','c','g','y']
label_array = ['null','index','middle','ring','little','thumb']
for i in range(6):
	axes.scatter(compressed_data[i*batch*loop_num:(i+1)*batch*loop_num,0],compressed_data[i*batch*loop_num:(i+1)*batch*loop_num,1],color=color_array[i],label=label_array[i])


plt.legend(loc=3)
plt.show()



#clf = classifier_train(train_data,target_data,classifier='svm')