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
import logger_print as log

#-------------------------------------- Init Part
# ACM for arduino, USB for stm32
def serial_init():
    if 'Linux' in platform.platform():
        try:
            # print("using USB0")
            com1 = serial.Serial(
                '/dev/ttyUSB0',
                # '/dev/ttyUSB2',

                115200,
                timeout=3,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE)
        except:
            # print("using ACM0")
            com1 = serial.Serial(
                '/dev/ttyACM0',
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
global cameraCapture
log_info = log.logger.info



#-------------------------------------- Init Part End


# -------------------------------------- Mseeage Part
def isComplete(serial):
    s = serial.readline()
    # print("waiting for feedback...", s)
    log_info("waiting for feedback...{}".format(s))
    if b'K' in s:
        # print("complete!\n--------------------------------------")
        log_info("complete!\n--------------------------------------")
        return True

# Decoator will throw an exception and finish all program when error occurs 
# Function: wait 5s for finish RB_Class _Send()
# @func_set_timeout(5)
def RB_Class_Send(serial_wheel,ClsNum=0):
    pathw = str(ClsNum)
    # pathw = "s"
    serial_wheel.write(pathw.encode("utf-8"))
    # print("RB Class Send : {}\n---------------------------------".format(ClsNum))
    log_info("RB Class Send : {}\n---------------------------------".format(ClsNum))
    # ** 
    if(ClsNum is 'c' or ClsNum is 5):
        try:
            while (True):
                if isComplete(serial_wheel) == True:
                    break
        except Exception as e: 
            print("Erroe:timeout(3)")
        # traceback.# print_exc()




# Send Message
def SendMessage(rubbish_class,_max_conf=0):
    if not my_serial.isOpen():
        my_serial.open()
    try:
        RB_Class_Send(my_serial,rubbish_class[_max_conf])
    except Exception as e:
        # print("error func_timeout(5) overcome! Resending!")
        log.logger.error("error func_timeout(5) overcome! Resending!\n" + str(e))
        # RB_Class_Send(my_serial,rubbish_class)


# -------------------------------------- Mseeage Part End

# -------------------------------------- Camera Part
def camera_check():
    cam_max_num = 4
    for device in range(0, cam_max_num):
        stream = cv2.VideoCapture(device)
        grabbed = stream.grab()
        if grabbed:
            # print("use camera device: " + str(device))
            log_info("use camera device: " + str(device))
            return device
    return -1

def camera_init():
    global cameraCapture

    cam_present_num = camera_check()
    if cam_present_num == -1:
        # print("camera start failed")
        log.logger.error("camera start failed")
        exit(0)

    cameraCapture = cv2.VideoCapture(cam_present_num)
#
def take_pic(mode=1):
    global cameraCapture

    # success, imagemiddle = cameraCapture.read()
    # time.sleep(5)
    time.sleep(1)
    # print("拍摄中－－－－－－－－－－－－－－－－－－－－")
    log_info("拍摄中－－－")
    for i in range(15):
        success, imagemiddle = cameraCapture.read()
    cv2.destroyAllWindows()

    cv2.imwrite('/home/ubuntu/python_pro/A_polyp/pic_save/laji.jpg',imagemiddle)
    global list_num
    cv2.imwrite('/home/ubuntu/python_pro/A_polyp/pic/ori' + str(list_num) + '.jpg', imagemiddle)
    list_num +=1
    # print("拍照完成－－－－－－－－－－－－－－－－－－－－－－")
    log_info("拍照完成－－－")
    return imagemiddle

# -------------------------------------- Camera Part End


# -------------------------------------- Detect Part
def add_num():
    global time_num
    time_num += 1
    if time_num % 2 == 0 and time_num > 0:
        pv.Main_text.NAME = "砖瓦石头"
        
        SendMessage([4])

def take_detect():
    global time_num
    #* open camera
    take_pic()

    # for i in range(3):
    #flag, image, rubbish_class = Detect(net,LABELS,COLORS,image_path)
    try:
        flag, rubbish_class,_max_conf = ec.Easydl_Cpp()

        # traceback.# print_exc()
        if flag:
            time_num = 0
            pv.showText()
            if rubbish_class[_max_conf] != 5 and rubbish_class[_max_conf] != 0:
                SendMessage(rubbish_class,_max_conf)
        elif not flag:
            add_num()
            take_pic()
            flag_2,rubbish_class,_max_conf = ec.Easydl_Cpp()
            if flag_2:
                time_num = 0
                pv.showText()
                if rubbish_class[_max_conf] != 5 and rubbish_class[_max_conf] != 0:
                    SendMessage(rubbish_class,_max_conf)
            elif not flag_2:
                add_num()
    except Exception as e:
        traceback.print_exc()
        log.logger.error("detect error:" + str(e))
        # time.sleep(1)
    #*unlimit loop
    # take_detect()

# Mian Detect start
def detect(): 
    global detect_num
    while True:
        if(detect_num > 0):
            take_detect()
            detect_num -= 1

# -------------------------------------- Detect Part End


# -------------------------------------- Message Listen Part (Main)
# Main Core Start
def pylisten(serial):
    global detect_num
    while True:
        s = serial.readline()
        if s :
            # print("rec:"+str(s))
            log_info("receive message: " +  str(s))
            if b's' in s or b'S' in s:
                detect_num += 1

# -------------------------------------- Message Listen Part End




def WarnUp():
    global my_serial
    flag, _ ,_= ec.Easydl_Cpp(0)
    if(flag and my_serial.isOpen()):
        return True
    else:
        return False

# 0 is safe 
# 5 is failed 
if __name__ == '__main__':
    # print("start\n")
    log_info("system start!")
    camera_init()
    if(WarnUp()):   
        SendMessage(['c'])
    else:
        SendMessage([5])

    t1 = threading.Thread(target=pylisten,args=(my_serial,))
    t1.start()

    t2 = threading.Thread(target=detect)
    t2.start()
    t3 = threading.Thread(target=pv.playvedio)
    t3.start()
    
    # t4 = threading.Thread(target=pv.playSound)
    # t4.start()
    pv.win.mainloop()
    # RB_Class_Send must be surrounded by try ... except Exception as e
    # for non-blocking receving a reply
    # try:
    #     RB_Class_Send(my_serial)
    # except Exception as e:
    #     time.sleep(3)
    #     # print("time delay 3s")
    #     RB_Class_Send(my_serial)
    # list_port = list(serial.tools.list_ports.comports())
    # # print(list_port)



