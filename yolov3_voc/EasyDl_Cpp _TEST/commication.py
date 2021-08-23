import serial
import time
import platform
import traceback
from func_timeout import func_set_timeout
import serial.tools.list_ports
import threading
import playVedio as pv
import numpy as np
import cv2
import time
import os
import EasyDL_cpp as ec


def serial_init():
    if 'Linux' in platform.platform():
        try:
            print("using ACM0")
            com1 = serial.Serial(
                '/dev/ttyACM0',
                # '/dev/ttyUSB2',

                115200,
                timeout=3,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE)
        except:
            print("using ACM1")
            com1 = serial.Serial(
                '/dev/ttyACM1',
                # '/dev/ttyUSB2',

                115200,
                timeout=3,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE)


    elif 'Windows' in platform.platform():
        com1 = serial.Serial(
            'COM60',
            115200,
            timeout=2,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE)

    else:
        raise RuntimeError('Unsupported platform.')

    time.sleep(1)
    wheel_com = com1

    return wheel_com

# init
detect_num = 0
my_serial = serial_init()
list_num = 0
time_num=0



# Decoator will throw an exception and finish all program when error occurs 
# Function: wait 5s for finish RB_Class _Send()
# @func_set_timeout(5)
def RB_Class_Send(serial_wheel,ClsNum=0):
    pathw = "RB:"+str(ClsNum)
    # pathw = "s"
    serial_wheel.write(pathw.encode("utf-8"))
    print("RB Class Send : {}\n---------------------------------".format(ClsNum))
    try:
        while (True):
            if isComplete(serial_wheel) == True:
                break
    except: 
        print("Erroe:timeout(5)")
        # traceback.print_exc()


def isComplete(serial):
    s = serial.readline()
    print("waiting for feedback...", s)
    if b'K' in s:
        print("complete!\n--------------------------------------")
        return True


# Send Message
def SendMessage(rubbish_class):
    if not my_serial.isOpen():
        my_serial.open()
    try:
        RB_Class_Send(my_serial,rubbish_class)
    except:
        print("error func_timeout(5) overcome! Resending!")
        # RB_Class_Send(my_serial,rubbish_class)

    print("send:: {}".format(rubbish_class))
    if rubbish_class is 1:
        pv.Main_text.COUNT += 1
        pv.Main_text.CATEGOARY = "厨余垃圾"
        pv.numberofRubbish.kinchenBin += 1
    elif rubbish_class is 2:
        pv.Main_text.COUNT += 1
        pv.Main_text.CATEGOARY = "有害垃圾"
        pv.numberofRubbish.harmfulBin += 1
    elif rubbish_class is 3:
        pv.Main_text.COUNT += 1
        pv.Main_text.CATEGOARY = "可回收垃圾"
        pv.numberofRubbish.recyclabelsBin += 1
    elif rubbish_class is 4:
        pv.Main_text.COUNT += 1
        pv.Main_text.CATEGOARY = "其他垃圾"
        pv.numberofRubbish.otherBin += 1






#
def take_pic():
    time.sleep(2)
    print("拍摄中－－－－－－－－－－－－－－－－－－－－")
    cameraCapture = cv2.VideoCapture(0)
    # success, imagemiddle = cameraCapture.read()
    # time.sleep(5)
    for i in range(15):
        success, imagemiddle = cameraCapture.read()
    cv2.destroyAllWindows()

    cv2.imwrite('/home/ubuntu/python_pro/A_polyp/pic_save/laji.jpg',imagemiddle)
    global list_num
    cv2.imwrite('/home/ubuntu/python_pro/A_polyp/pic/laji' + str(list_num) + '.jpg', imagemiddle)
    list_num +=1
    print("拍照完成－－－－－－－－－－－－－－－－－－－－－－")
    return imagemiddle

def add_num():
    global time_num
    time_num += 1
    if time_num % 3 == 0 and time_num > 0:
        pv.Main_text.NAME = "砖瓦石头"
        SendMessage('4')

def take_detect():
    global time_num
    #* open camera
    take_pic()

    # for i in range(3):
    #flag, image, rubbish_class = Detect(net,LABELS,COLORS,image_path)
    flag, rubbish_class = ec.Easydl_Cpp()
    if flag:
        time_num = 0
        pv.showText()
        if rubbish_class != 5:
            SendMessage(rubbish_class)
    else:
        add_num()
        # time.sleep(1)
    #*unlimit loop
    # take_detect()



# Main Core Start
def pylisten(serial):
    global detect_num
    while True:
        s = serial.readline()
        if s :
            print("rec:"+str(s))
            if b'S' in s:
                detect_num += 1

def detect():
    global detect_num
    while True:
        if(detect_num > 0):
            take_detect()
            detect_num -= 1





# 
if __name__ == '__main__':
    print("start\n")

    t1 = threading.Thread(target=pylisten,args=(my_serial,))
    t1.start()

    t2 = threading.Thread(target=detect)
    t2.start()
    t3 = threading.Thread(target=pv.playvedio)
    t3.start()

    pv.win.mainloop()
    # RB_Class_Send must be surrounded by try ... except
    # for non-blocking receving a reply
    # try:
    #     RB_Class_Send(my_serial)
    # except:
    #     time.sleep(3)
    #     print("time delay 3s")
    #     RB_Class_Send(my_serial)
    # list_port = list(serial.tools.list_ports.comports())
    # print(list_port)



