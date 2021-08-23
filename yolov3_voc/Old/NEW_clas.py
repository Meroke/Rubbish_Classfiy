import numpy as np
import cv2
import time
import os
import threading
import EasyDL_detect as ea
import EasyDL_cpp as ec
import playVedio as pv

list_num = 0
time_num=0
def SendMessage(rubbish_class):
    print("send:: {}".format(rubbish_class))
    if not ea.ser.isOpen():
        ea.ser.open()
    if rubbish_class is 1:
        ea.ser.write(b'1')
        # ser.flushInput()
        pv.Main_text.COUNT += 1
        pv.Main_text.CATEGOARY = "厨余垃圾"
        pv.numberofRubbish.kinchenBin += 1
    elif rubbish_class is 2:
        ea.ser.write(b'2')
        # ser.flushInput()
        pv.Main_text.COUNT += 1
        pv.Main_text.CATEGOARY = "有害垃圾"
        pv.numberofRubbish.harmfulBin += 1
    elif rubbish_class is 3:
        ea.ser.write(b'3')
        # ser.flushInput()
        pv.Main_text.COUNT += 1
        pv.Main_text.CATEGOARY = "可回收垃圾"
        pv.numberofRubbish.recyclabelsBin += 1
    elif rubbish_class is 4:
        ea.ser.write(b'4')
        # ser.flushInput()
        pv.Main_text.COUNT += 1
        pv.Main_text.CATEGOARY = "其他垃圾"
        pv.numberofRubbish.otherBin += 1



#
def take_pic():
    time.sleep(5)
    print("拍摄中－－－－－－－－－－－－－－－－－－－－")
    cameraCapture = cv2.VideoCapture(1)
    # success, imagemiddle = cameraCapture.read()
    # time.sleep(5)
    for i in range(15):
        success, imagemiddle = cameraCapture.read()
    cv2.destroyAllWindows()
    cv2.imwrite('../pic_save/laji.jpg',imagemiddle)
    global list_num
    cv2.imwrite('../pic_save_every/laji' + str(list_num) + '.jpg', imagemiddle)
    list_num +=1
    print("拍照完成－－－－－－－－－－－－－－－－－－－－－－")
    return imagemiddle

def add_num():
    global time_num
    time_num += 1
    if time_num % 3 == 0 and time_num > 0:
        pv.Main_text.NAME = "砖瓦石头"
        SendMessage(4)

def take_detect():
    global time_num
    take_pic()

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
    take_detect()


if __name__ == "__main__":
    print("启动等待2s")
    time.sleep(2)
    p1 = threading.Thread(target=pv.playvedio)
    # p1.setDaemon(True)
    p1.start()
    # p2 = threading.Thread(target=pv.showText)
    # p2.start()
    p3 = threading.Thread(target=take_detect)
    # p3.setDaemon(True)
    p3.start()
    p4 = threading.Thread(target=pv.playSound)
    # p4.setDaemon(True)
    p4.start()

    # p5 = threading.Thread(target=recvMessage)
    # p5.start()

    pv.win.mainloop()
    # while 1:
    #     open_sign()
