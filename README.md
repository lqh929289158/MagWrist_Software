# MagWrist_Software

## About MagWrist
This is a project created by **QINGHAO LIU**.
The basic idea is that:

The program of the system has two parts: Hardware(Embedded Board) and Software(PC).

This README _Only_ talks about **Software** part.

## Overview

The software part is based on Python. If you are not familiar with it, please learn about it by yourself(REALLY EASY).

This repository contains many files, which are almost independent on each other.

- RealTimeShow.py
- RealTimeShow_Relative.py

## Python Environment

No matter which OS(MacOS,Win,Unix,Linux) you are using, you are strongly recommended to run the program in **Terminal**.

1. Install Python3(There may be some problems with Python2, so please kindly use Python3). You can download it [here](https://www.python.org/downloads/). Confirm you have installed python3 successfully.
   - MacOS: Open **Terminal**. Type `python3`. If you can enter the shell, congratulations!
   - Win/Linux: Open **Terminal**. Type `python`. If you can enter the shell, congratulations!

2. Install Pip. Maybe the installation program above has installed pip for you. Confirm it:
   - MacOS: Open **Terminal**. Type `pip3 -V`. If the version number shows up, congratulations!
   - Win/Linux: Open **Terminal**. Type `pip -V`. If the version number shows up, congratulations!
   Otherwise, Google how to install pip for your PC.
3. Install packages needed by pip.

(For MacOS, replace `pip` with `pip3`)
```
pip install numpy
pip install matplotlib
pip install pyserial
pip install serial
pip install sklearn
```
## Find the serial port name of your device.

Open **Terminal**. Type the code as below(For MasOS, replace `python` with `python3`):
```
python -m serial.tools.list_ports
```
If no problem, you can see a list of serial port names of your PC.

Then, connect the embedded board to your PC by a microUSB-USB or microUSB-USB(Type-C) wire.

Execute the commmand above again. Please find out the new added port name.
- For MacOS: The port name format looks like this _/dev/cu.usbmodem0F00577F_
- For Win: The port name format looks like this _COM1_

## Start with RealTimeShow.py First!

This is a Real-time program that can plot the data of 10 magnetometers and 1 motion sensor vividly!

1. Modify port name. Open **RealTimeShow.py** with the editor you prefer. Find the code below:
```
ser = serial.Serial('/dev/cu.usbmodem0F00577F',1500000)
```
Replace the `/dev/cu.usbmodem0F00577F` with the port name of your device. For example:
```
ser = serial.Serial('COM3',1500000)
```
The second parameter `1500000` is clock frequency of UART. Please keep it the same with the hardware part. If you have no extra requirement, you do not need to change it.

2. Open **Teriminal** and locate to the repository. Execute the command below:

(For MacOS, replace `python` with `python3`)
```
python RealTimeShow.py
```

3. If you can see a dynamic figure like this, congratulations!(Please try moving or rotating the magnetometer array to observe the curve)
![RealTimeShow_Example](RealTimeShow_Example.png)

Explanation:
   - There are 11 windows, 10 around for magnetometers, 1 in middle for motion sensors.
   - In each magetometer window, there are 3 lines, **Blue for X-axis** data, **Orange for Y-axis** data, **Green for Z-axis** data.
   - In motion-sensor window, there would be 6 lines, 3 for accelermeter, 3 for gyroscope(Not shown on the picture).
   - The range of vertical axis will change automatically with the max and min value of the data so that you can watch it elegantly.
   - The range of horizontal axis will change periodically to subsitute new data for old data.
   
Possible problem:
   - All three lines of a magnetometer may keep constant(0/+-1024/+-2048)(See Right-Up side of the picture). Solution: **Check the connection between embedded board and magnetometer array**.
   - Some lines or data may be unstable and change dramatically. Solution: The same as above.
   - All lines become frozen suddenly. Solution: **Close the figure, re-connect embedded board, and try again**.
   - _**Only one of the line of a magnetometer keeps constant**_. That's the worst case. Probably your sensor chip has some problem. Unfortunately, there is no good solution until now but changing chip.
