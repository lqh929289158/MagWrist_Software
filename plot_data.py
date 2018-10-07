import numpy as np
from scipy import integrate
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.decomposition import KernelPCA
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import scipy as sp
import serial
import sys
import time

def draw_power_for_each_finger(single,interpol=None,norm='off',hand='left'):
	fig1 = plt.figure()	#for single

	fs_index	= fig1.add_subplot(511)
	fs_middle	= fig1.add_subplot(512)
	fs_ring		= fig1.add_subplot(513)
	fs_little	= fig1.add_subplot(514)
	fs_thumb	= fig1.add_subplot(515)

	fs_index.set_title('Index Finger')
	fs_middle.set_title('Middle Finger')
	fs_ring.set_title('Ring Finger')
	fs_little.set_title('Little Finger')
	fs_thumb.set_title('Thumb')
	if hand == 'left':
		index 	= [[col[0] for col in row[::-1]] for row in single]
		middle 	= [[col[1] for col in row[::-1]] for row in single]
		ring 	= [[col[2] for col in row[::-1]] for row in single]
		little 	= [[col[3] for col in row[::-1]] for row in single]
		thumb 	= [[col[4] for col in row[::-1]] for row in single]
	if hand == 'right':
		index 	= [[col[0] for col in row] for row in single]
		middle 	= [[col[1] for col in row] for row in single]
		ring 	= [[col[2] for col in row] for row in single]
		little 	= [[col[3] for col in row] for row in single]
		thumb 	= [[col[4] for col in row] for row in single]

	im_style = 'jet'
	#interpol = 'nearest'
	#interpol = 'bilinear'
	index_norm = None
	middle_norm = None
	ring_norm = None
	little_norm = None
	thumb_norm = None

	norm_min = 250
	norm_max = 500
	if norm=='on':
		index_norm = matplotlib.colors.Normalize(vmin=norm_min, vmax=norm_max)
		middle_norm = matplotlib.colors.Normalize(vmin=norm_min, vmax=norm_max)
		ring_norm = matplotlib.colors.Normalize(vmin=norm_min, vmax=norm_max)
		little_norm = matplotlib.colors.Normalize(vmin=norm_min, vmax=norm_max)
		thumb_norm = matplotlib.colors.Normalize(vmin=norm_min, vmax=norm_max)

	im = fs_index.imshow(index,interpolation=interpol,cmap=im_style,norm=index_norm)
	fig1.colorbar(im,ax=fs_index)

	im = fs_middle.imshow(middle,interpolation=interpol,cmap=im_style,norm=middle_norm)
	fig1.colorbar(im,ax=fs_middle)

	
	im = fs_ring.imshow(ring,interpolation=interpol,cmap=im_style,norm=ring_norm)
	fig1.colorbar(im,ax=fs_ring)

	im = fs_little.imshow(little,interpolation=interpol,cmap=im_style,norm=little_norm)
	fig1.colorbar(im,ax=fs_little)
	
	im = fs_thumb.imshow(thumb,interpolation=interpol,cmap=im_style,norm=thumb_norm)
	fig1.colorbar(im,ax=fs_thumb)

	return fig1

f = open('finger_vectors_file_yifeng.txt','r')

s = f.readline()
s = s.split()
s = [int(item) for item in s]
row_num = s[0]
col_num = s[1]
print(s[0])
print(s[1])
single = []
for i in range(row_num):
	single.append([])
for i in range(row_num*col_num):
	if single[i//col_num]==[]:
		print('\n')
	finger_powers=[]
	for j in range(5):
		s = f.readline()
		s = s.split()
		while(s==[]):
			s = f.readline()
			s = s.split()
		
		#set the abnormal data as 0
		vec = [float(item) for item in s]
		for k in range(len(vec)):
			if abs(vec[k])>1000:
				vec[k] = 0
		#here to choose axes as you want
		#You can modify the code below as `vec = np.array(vec[3:])`
		#which means you throw the three axes of sensor 0
		vec = np.array(vec)
		veclen = np.linalg.norm(vec)
		print('%.3f'%veclen,end=" ")
		finger_powers.append(veclen)
	print(' ')
	
	single[i//col_num].append(finger_powers)
fig = draw_power_for_each_finger(single,interpol='bilinear',norm='off')


plt.show()