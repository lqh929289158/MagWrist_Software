import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial

ser = serial.Serial('/dev/cu.usbmodem0F00577F',1500000)

loop = 0
winlen = 50

sensor_num = 10
sensor_dim = 3 #XYZ

subplot_row = 4
subplot_col = 3

x = []


#create empty Mag_Array
Mag_Array = []

for i in range(sensor_num):
	Sensor_Dims = []
	for j in range(sensor_dim):
		Sensor_Dim_Vector=[0]
		Sensor_Dims.append(Sensor_Dim_Vector)
	Mag_Array.append(Sensor_Dims)

#create empty AccGyr_Array[6][time]
AccGyr_Array = []
for i in range(6):
	AccGyr_Array.append([])

fig=plt.figure()
#figure add subplot
axes_array = []
line_array = []

if(sensor_num==10):
	axes_array.append(fig.add_subplot(subplot_row,subplot_col,3))
	axes_array.append(fig.add_subplot(subplot_row,subplot_col,2))
	axes_array.append(fig.add_subplot(subplot_row,subplot_col,1))
	axes_array.append(fig.add_subplot(subplot_row,subplot_col,6))
	axes_array.append(fig.add_subplot(subplot_row,subplot_col,4))
	axes_array.append(fig.add_subplot(subplot_row,subplot_col,9))
	axes_array.append(fig.add_subplot(subplot_row,subplot_col,7))
	axes_array.append(fig.add_subplot(subplot_row,subplot_col,12))
	axes_array.append(fig.add_subplot(subplot_row,subplot_col,11))
	axes_array.append(fig.add_subplot(subplot_row,subplot_col,10))
	axes_array.append(fig.add_subplot(subplot_row,subplot_col,8))
else:
	for i in range(1,sensor_num+1):
		axes_array.append(fig.add_subplot(subplot_row,subplot_col,i))


#subplot draw line
templen = 100
for ax in axes_array[:-1]:
	temp = []
	for i in range(sensor_dim):

		lin,= ax.plot(range(templen))
		temp.append(lin)
	line_array.append(temp)

temp = []
for i in range(6):
	lin, = axes_array[-1].plot(range(templen))
	temp.append(lin)
line_array.append(temp)

def update(data):
	winlen = data[-1]
	loop = data[-2]
	start = data[-3]
	for i in range(sensor_num):
		for j in range(sensor_dim):
			line_array[i][j].set_xdata(range(start,start+len(data[i][j])))
			line_array[i][j].set_ydata(data[i][j])
	flatten = [item for row in line_array[:-1] for item in row]
	for j in range(6):
		line_array[-1][j].set_xdata(range(start,start+len(data[-4][j])))
		line_array[-1][j].set_ydata(data[-4][j])
		flatten.append(line_array[-1][j])
	return tuple(flatten)
def data_gen():
	cnt=0
	loop=0
	winlen = 100

	while True:
		cnt = cnt + 1
		x = range(loop*winlen,cnt)
		for i in range(sensor_num+1):
			s = ser.readline()
			if i == 0:
				print(s)
				print(cnt)
			s = s.decode()
			if len(s) == 23:#Three-data information(Magnetometer)
				s = s.split()
				try:
					for j in range(sensor_dim):
						Mag_Array[int(s[-1])][j].append(int(s[j]))
				except:
					print("int covertion fail!!!")
			elif len(s) == 44:#Six-data information(Motion sensor)
				s = s.split()
				try:
					for j in range(6):
						AccGyr_Array[j].append(int(s[j]))
				except:
					print("AccGyr Error!!!")

			if len(Mag_Array[0][0]) >winlen:
				loop = len(Mag_Array[0][0])//winlen
				for ax in axes_array:
					ax.set(xlim=[loop*winlen,(loop+1)*winlen])
		
		#choose a pivot and compute relative value(Change as you want)
		pivot = 3
		for i in range(sensor_num):
			if i == pivot:
				continue
			for j in range(sensor_dim):
				Mag_Array[i][j][-1] -= Mag_Array[pivot][j][-1]
		print(" ")

		if loop>0:
			start = loop*winlen-2
		else:
			start = loop*winlen

		for i in range(sensor_num):
			down = min([min(row[start:]) for row in Mag_Array[i]])
			up 	 = max([max(row[start:]) for row in Mag_Array[i]])
			axes_array[i].set(ylim=[ \
				down -(up-down)*0.05,\
				up 	 +(up-down)*0.05])
		
		#for acc and gyr
		down = min([min(row[start:]) for row in AccGyr_Array])
		up   = max([max(row[start:]) for row in AccGyr_Array])

		axes_array[-1].set(ylim=[ \
			down -(up-down)*0.05, \
			up 	 +(up-down)*0.05])

		data = [[np.array(dim[start:]) for dim in row] for row in Mag_Array]
		data.append([np.array(row[start:]) for row in AccGyr_Array])
		data.append(start)
		data.append(loop)
		data.append(winlen)
		yield data
ani = animation.FuncAnimation(fig, update, data_gen, interval=2)
plt.show()