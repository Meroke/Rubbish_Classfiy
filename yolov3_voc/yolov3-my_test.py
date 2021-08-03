# coding:utf-8
import numpy as np
import cv2
import time
import os
import sys
import threading
import playVedio as pv
import serial
import multiprocessing

port = "/dev/rfcomm2"
ser = serial.Serial(port,9600)

boxes = []
confidences = []
classIDs = []
# 1:厨余垃圾，2：可回收垃圾，3：有害垃圾，4:其他垃圾
rubbish = {'apple': 1, 'orange': 1, 'pear': 1, 'Bell pepper': 1, 'Cabbage': 1, 'Broccoli': 1, 'Carrot': 1, 'Potato': 1,\
           'banana':1,'garlic':1,'grape':1,'green':1, 'Tomato': 1, 'Cucumber': 1, 'Pumpkin': 1, 'Mushroom': 1, 'pea':1,'onion':1,'whiteradish':1,\
           'can': 2, 'bottle': 2, \
           'batttery': 3,\
           'blank': 5}

ChineseName = {'apple':'苹果', 'orange': '橘子', 'pear': '梨', 'Bell pepper': '青椒', 'Cabbage': '卷心菜', 'Broccoli': '西兰花', 'Carrot': '萝卜', 'Potato': '土豆',\
           'banana':'香蕉','garlic':'大蒜','grape':'葡萄','green':'青菜', 'Tomato': '番茄', 'Cucumber': '黄瓜', 'Pumpkin': '南瓜', 'Mushroom': '蘑菇', 'pea':'豌豆','onion':'洋葱','whiteradish':'萝卜',\
           'can': '易拉罐', 'bottle': '瓶子', \
           'batttery': '电池',\
           }
rubbish_class = 0  # 默认无垃圾


class detector:
    def __init__(self):
        self.weightsPath = '../weights/yolov3-big.weights'  # 模型权重文件
        self.configPath = "../weights/yolov3-big.cfg"  # 模型配置文件
        self.labelsPath = "../weights/classes.names"  # 模型类别标签文件


def return_rubbish_class(seq,LABELS):
    key = LABELS[classIDs[seq]]
    if key in rubbish:
        return rubbish[key]
    else:
        return 0


def SendMessage(rubbish_class):
    print("send:: {}".format(rubbish_class))
    if not ser.isOpen():
        ser.open()
    if rubbish_class is 1:
        ser.write(b'1')
        ser.flushInput()
        pv.Main_text.COUNT += 1
        pv.Main_text.CATEGOARY = "厨余垃圾"
    elif rubbish_class is 2:
        ser.write(b'2')
        ser.flushInput()
        pv.Main_text.COUNT += 1
        pv.Main_text.CATEGOARY = "可回收垃圾"
    elif rubbish_class is 3:
        ser.write(b'3')
        ser.flushInput()
        pv.Main_text.COUNT += 1
        pv.Main_text.CATEGOARY = "有害垃圾"
    elif rubbish_class is 4:
        ser.write(b'4')
        ser.flushInput()
        pv.Main_text.COUNT += 1
        pv.Main_text.CATEGOARY = "其他垃圾"


def take_pic():
    time.sleep(2)
    print("拍摄中－－－－－－－－－－－－－－－－－－－－")
    cameraCapture = cv2.VideoCapture(1)
    success, imagemiddle = cameraCapture.read()
    # time.sleep(5)
    for i in range(35):
        success, imagemiddle = cameraCapture.read()

    # cv2.imshow("original", imagemiddle)
    cv2.imwrite("shopping_pic.jpg", imagemiddle)
    print("拍照完成－－－－－－－－－－－－－－－－－－－－－－")
    return imagemiddle

def Detect() -> object:
    # global p3
    Detor = detector();

    # 初始化一些参数
    LABELS = open(Detor.labelsPath).read().strip().split("\n")
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")  # 随机生成颜色框

    # 加载 网络配置与训练的权重文件 构建网络
    net = cv2.dnn.readNetFromDarknet(Detor.configPath, Detor.weightsPath)
    # ser = serial.Serial("/dev/ttyACM0", 9600, timeout=1) # mark

    #
    image = take_pic()
    # 读入待检测的图像
    #image = cv2.imread('E:/_TempPhoto/JPEGImages/g1.jpg')

    # 得到图像的高和宽
    (H, W) = image.shape[0:2]


    # 得到 YOLO需要的输出层
    ln = net.getLayerNames()
    out = net.getUnconnectedOutLayers()  # 得到未连接层得序号  [[200] /n [267]  /n [400] ]
    x = []
    for i in out:  # 1=[200]
        x.append(ln[i[0] - 1])  # i[0]-1    取out中的数字  [200][0]=200  ln(199)= 'yolo_82'
    ln = x
    # ln  =  ['yolo_82', 'yolo_94', 'yolo_106']  得到 YOLO需要的输出层

    # 从输入图像构造一个blob，然后通过加载的模型，给我们提供边界框和相关概率
    # blobFromImage(image, scalefactor=None, size=None, mean=None, swapRB=None, crop=None, ddepth=None)
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True,
                                 crop=False)  # 构造了一个blob图像，对原图像进行了图像的归一化，缩放了尺寸 ，对应训练模型
    net.setInput(blob)  # 将blob设为输入？？？ 具体作用还不是很清楚
    layerOutputs = net.forward(ln)  # ln此时为输出层名称  ，向前传播  得到检测结果

    for output in layerOutputs:  # 对三个输出层 循环
        for detection in output:  # 对每个输出层中的每个检测框循环
            scores = detection[5:]  # detection=[x,y,h,w,c,class1,class2] scores取第6位至最后
            classID = np.argmax(scores)  # np.argmax反馈最大值的索引
            confidence = scores[classID]
            if confidence > 0.5:  # 过滤掉那些置信度较小的检测结果
                box = detection[0:4] * np.array([W, H, W, H])
                # print(box)
                (centerX, centerY, width, height) = box.astype("int")
                # 边框的左上角
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                # 更新检测出来的框
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.3)
    try:
        box_seq = idxs.flatten()  # [ 2  9  7 10  6  5  4]
    except AttributeError:
        print("识别失败－－－－－－－－－－－－－－")
        exit()
        # p2.join()
        # p2 = threading.Timer(5, Detect)
        # p2.start()
        # Detect()

    if len(idxs) > 0:
        rubbish_class = 0
        for seq in box_seq:
            rubbish_class = return_rubbish_class(seq,LABELS)
            if rubbish_class != 5:
                if rubbish_class != 1 and rubbish_class != 2 and  rubbish_class != 3:
                    rubbish_class = 4

            (x, y) = (boxes[seq][0], boxes[seq][1])  # 框左上角
            (w, h) = (boxes[seq][2], boxes[seq][3])  # 框宽高
            color = COLORS[classIDs[seq]].tolist()
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 1)  # 画框
            text = "{}: {:.4f}".format(LABELS[classIDs[seq]], confidences[seq])
            print("======" + str(text) + "======")
            cv2.putText(image, ChineseName[text], (x, y - 5), cv2.FONT_HERSHEY_DUPLEX, 1, color, 1)  # 写字
        SendMessage(rubbish_class)

    cv2.namedWindow('img', cv2.WINDOW_NORMAL)

    # cv2.imshow("img", image)
    cv2.imwrite("最终结果.jpg", image)
    # cv2.waitKey(1)
    cv2.destroyAllWindows()
    # try:

    # for i in range(0,190000):
    #     pass

    # p4 = threading.Timer(5,Detect)
    # p4.start()

    # except:
    #     print('Detect is error')

# def open_sign():
#     sign = ser.readline()
#     if sign == 'open':

    # Detect()
def StartDetect():
    while 1:
        Detect()
        for i in range(2000):
            pass

class myThread_1(threading.Thread):
    def __init__(self, threadID, name, counter):
        super(myThread_1, self).__init__()
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.run()

    def run(self):
        print(self.name + " Starting")
        pv.playvedio()
        # test()
        print(self.name + " Ending")

class myThread_2(threading.Thread):
    def __init__(self, threadID, name, counter):
        super(myThread_2, self).__init__()
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print(self.name + " Starting")
        pv.showText()
        print(self.name + " Ending")

class myThread_3(threading.Thread):
    def __init__(self, threadID, name, counter):
        super(myThread_3, self).__init__()
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print(self.name + " Starting")
        Detect()
        print(self.name + " Ending")


class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        if self.threadID == 1:
            self.playVideo()
        elif self.threadID == 2:
            self.ShowText()
        elif self.threadID == 3:
            self.detect()

    def playVideo(self):
        print(self.name + " Starting")
        pv.playvedio()
        print(self.name + " Ending")

    def ShowText(self):
        print(self.name + " Starting")
        pv.showText()
        print(self.name + " Ending")

    def detect(self):
        print(self.name + " Starting")
        Detect()
        print(self.name + " Ending")

def test():
    print("test\ntest")

if __name__ == "__main__":
    # p1 = threading.Thread(target=pv.playvedio)
    # p1.setDaemon(True)
    # p1.start()
    # p2 = threading.Thread(target=pv.showText)
    # p2.setDaemon(True)
    # p2.start()
    # p3 = threading.Thread(target=Detect)
    # p3.setDaemon(True)
    # p3.start()

    # p1 = multiprocessing.Process(target=pv.playvedio)
    # p2 = multiprocessing.Process(target=pv.showText)
    # p3 = multiprocessing.Process(target=Detect)
    # p1.start()
    # p2.start()
    # p3.start()
    # th1 = myThread_1(1,'Thread_1',1)
    # th1.start()
    # th2 = myThread_2(2, 'Thread_2', 2)
    # th2.start()
    th3 = myThread_3(3, 'Thread_3', 3)

    # th1.start()
    # th2.start()
    th3.start()

    # th1.join()
    # th2.join()
    th3.join()
    # th2.ShowText()
    # th1.playVideo()
    # th3.detect()


    # pv.win.mainloop()
    # while 1:
    #     open_sign()

