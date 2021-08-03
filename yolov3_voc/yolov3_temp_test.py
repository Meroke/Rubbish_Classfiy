# coding:utf-8
import numpy as np
import cv2
import time
import os
import threading
import playVedio as pv
import serial

# 串口初始化
# port = "/dev/rfcomm2"
port = "/dev/rfcomm3"
ser = serial.Serial(port, 9600)

# 图片存储地址
image_path = '../pic_save/laji.jpg'

# 全局数值初始化
list_num = 0
photo_count = 0
boxes = []
confidences = []
classIDs = []
time_num = 0
# 1:厨余垃圾，2：有害垃圾，3：可回收垃圾，4:其他垃圾
rubbish = {'apple': 1, 'orange': 1, 'pear': 1, 'broccoli': 1, 'carrot': 1, 'potato': 1, 'blackBanana': 1, \
           'banana': 1, 'banana_peel': 1, 'garlic': 1, 'grape': 1, 'singlegrape': 1, 'green': 1, 'tomato': 1,\
           'cucumber': 1,\
           'pea': 1, 'multpea': 1, 'onion': 1, 'whiteradish': 1, 'hmg': 1, 'longyan': 1, 'mongo': 1, 'oil_orange': 1,\
           'baicai': 1, \
           'can': 3, 'can_end': 3, 'bottle': 3,'bottle_label': 3, \
           'battery': 2, 'battery_end': 2,'battery5': 2, \
           'cigarette': 4, \
           'blank': 5}

ChineseName = {'apple': '苹果', 'orange': '橘子', 'pear': '梨', 'broccoli': '西兰花', 'carrot': '萝卜', 'potato': '土豆',\
               'blackBanana': '香蕉', \
               'banana': '香蕉', 'banana_peel': '香蕉', 'garlic': '大蒜', 'grape': '葡萄', 'singlegrape': '葡萄', 'green': '青菜',\
               'tomato': '番茄', 'cucumber': '黄瓜', \
               'pea': '豌豆', 'multpea': '豌豆', 'onion': '洋葱', 'hmg': '哈密瓜', 'whiteradish': '萝卜', 'longyan': '龙眼',\
               'mongo': '芒果', 'oil_orange': '橘子', 'baicai': '白菜', \
               'can': '易拉罐', 'can_end': '易拉罐', 'bottle': '瓶子', 'bottle_label':'瓶子',\
               'battery': '电池', 'battery_end': '电池','battery5':'电池' ,\
               'cigarette': '香烟', \
               'blank': '白板'}

rubbish_class = 0  # 默认无垃圾


def Clear_all():
    boxes.clear()
    confidences.clear()
    classIDs.clear()


# class detector:
#     def __init__(self):
#         self.weightsPath = '../weights2/yolov3-big2.weights'  # 模型权重文件
#         self.configPath = "../weights2/yolov3-big.cfg"  # 模型配置文件
#         self.labelsPath = "../weights2/classes.names"  # 模型类别标签文件

# class detector_config_for_All:
#     def __init__(self):
#         self.weightsPath = '../weights_6000/my-v3_506000.weights'  # 模型权重文件
#         self.configPath = "../weights_6000/my-v3.cfg"  # 模型配置文件
#         self.labelsPath = "../weights_6000/classes.names"  # 模型类别标签文件

class detector_config_for_All:
    def __init__(self):
        self.weightsPath = '../weights_blank/my-v3_515000.weights'  # 模型权重文件
        self.configPath = "../weights_blank/my-v3.cfg"  # 模型配置文件
        self.labelsPath = "../weights_blank/classes.names"  # 模型类别标签文件
class detector_config_just_blank:
    def __init__(self):
        self.weightsPath = '../weights_justBlank/my-v3.backup'  # 模型权重文件
        self.configPath = "../weights_justBlank/my-v3.cfg"  # 模型配置文件
        self.labelsPath = "../weights_justBlank/classes.names"  # 模型类别标签文件

# class detector_config_for_All:
#     def __init__(self):
#         self.weightsPath = '../weights_blank/my-v3_515000.weights'  # 模型权重文件
#         self.configPath = "../weights_blank/my-v3.cfg"  # 模型配置文件
#         self.labelsPath = "../weights_blank/classes.names"  # 模型类别标签文件

class detector_config_for_Battery:
    def __init__(self):
        self.weightsPath = '../weights_forB/my-v3_forB_final.weights'  # 模型权重文件
        self.configPath = "../weights_forB/my-v3_forB.cfg"  # 模型配置文件
        self.labelsPath = "../weights_forB/classes.names"  # 模型类别标签文件

class detector_config_for_Bottle:
    def __init__(self):
        self.weightsPath = '../weights_BO/my-v3_forBO_final.weights'  # 模型权重文件
        self.configPath = "../weights_BO/my-v3_forBO.cfg"  # 模型配置文件
        self.labelsPath = "../weights_BO/classes_forBO.names"  # 模型类别标签文件

def return_rubbish_class(seq, LABELS):
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
        # ser.flushInput()
        pv.Main_text.COUNT += 1
        pv.Main_text.CATEGOARY = "厨余垃圾"
        pv.numberofRubbish.kinchenBin += 1
    elif rubbish_class is 2:
        ser.write(b'2')
        # ser.flushInput()
        pv.Main_text.COUNT += 1
        pv.Main_text.CATEGOARY = "有害垃圾"
        pv.numberofRubbish.harmfulBin += 1
    elif rubbish_class is 3:
        ser.write(b'3')
        # ser.flushInput()
        pv.Main_text.COUNT += 1
        pv.Main_text.CATEGOARY = "可回收垃圾"
        pv.numberofRubbish.recyclabelsBin += 1
    elif rubbish_class is 4:
        ser.write(b'4')
        # ser.flushInput()
        pv.Main_text.COUNT += 1
        pv.Main_text.CATEGOARY = "其他垃圾"
        pv.numberofRubbish.otherBin += 1


def recvMessage():
    if not ser.isOpen():
        ser.open()
    flag, num = ser.readline().split(b' ', 1)
    flag = flag.decode('utf8')
    num = ''.join(num.decode('utf8').split())  # 分割信息，默认空格分割
    if flag is 'Y':
        pv.Main_text.FULL_LOAD_FLAG = True
    else:
        pv.Main_text.FULL_LOAD_FLAG = False
    # 显示满载信息
    pv.showText2(int(num))


#
def take_pic():
    time.sleep(3)
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


def Detect(net,LABELS,COLORS,image_path) -> object:
    # 返回值 初始化
    detect_flag = 0
    rubbish_class= 0

    # global p3
    # 初始化一些参数

    # 加载 网络配置与训练的权重文件 构建网络
    # ser = serial.Serial("/dev/ttyACM0", 9600, timeout=1) # mark

    #
    Clear_all()
    image = cv2.imread(image_path)
    # 读入待检测的图像
    # image = cv2.imread('E:/_TempPhoto/JPEGImages/g1.jpg')

    # 得到图像的高和宽
    (H, W) = image.shape[0:2]

    # 得到 YOLO需要的输出层
    ln = net.getLayerNames()
    out = net.getUnconnectedOutLayers()  # 得到未连接层得序号  [[200] /n [267]  /n [400] ]
    x = []
    for i in out:  # 1=[200]
        x.append(ln[i[0] - 1])  # i[0]-1    取out中的数字  [200][0]=200  ln(199)= 'yolo_82'
    ln = x
    # ln  =  ['yolo_82', 'yolo_94', 'yolo_106']  得到 YOLO需要的输出层6

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
            if confidence > 0.40:  # 过滤掉那些置信度较小的检测结果
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

        if len(idxs) > 0:
            rubbish_class = 0
            for seq in box_seq:
                rubbish_class = return_rubbish_class(seq, LABELS)
                if rubbish_class != 5:  # 不是白板
                    if rubbish_class != 1 and rubbish_class != 2 and rubbish_class != 3:  # 不在记录中的垃圾全部识别为其他垃圾
                        rubbish_class = 4

                (x, y) = (boxes[seq][0], boxes[seq][1])  # 框左上角
                (w, h) = (boxes[seq][2], boxes[seq][3])  # 框宽高
                color = COLORS[classIDs[seq]].tolist()
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 1)  # 画框
                text = "{}: {:.4f}".format(LABELS[classIDs[seq]], confidences[seq])
                print("======" + str(text) + "======")
                # 获取垃圾具体中文名称
                pv.Main_text.NAME = ChineseName[str(LABELS[classIDs[seq]])]
                # 在图像上标注垃圾种类
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_DUPLEX, 1, color, 1)  # 写字
                detect_flag = 1

    except AttributeError:
        print("识别失败－－－－－－－－－－－－－－")
        # exit()
        # SendMessage(4)
        # time.sleep(4)
        # Detect()

        # p2.join()
        # p2 = threading.Timer(5, Detect)
        # p2.start()
        # Detect()

        # if rubbish_class != 5:
        #     SendMessage(rubbish_class)
        # reName_class = rubbish_class

    # mark 测试为了检测是否能够成功显示满载检测的信息
    # pv.test_for_number()

    # cv2.namedWindow('img', cv2.WINDOW_NORMAL)

    global photo_count
    # cv2.imshow("img", image)
    cv2.imwrite('../pic/' + 'detect1' + str(photo_count) + ".jpg", image)
    photo_count += 1

    # cv2.waitKey(0)
    cv2.destroyAllWindows()
    time.sleep(2)

    return detect_flag, image, rubbish_class
    # p4 = threading.Timer(5,Detect)
    # p4.start()

    # except:
    #     print('Detect is error')


# def open_sign():
#     sign = ser.readline()
#     if sign == 'open':

# Detect()
# def take_detect():
#     take_pic()
#     flag, image, rubbish_class = Detect(net2,LABELS2,COLORS,image_path)
#     if flag:
#         pv.showText()
#         if rubbish_class != 5:
#             SendMessage(rubbish_class)
#         time.sleep(2)
#     else:
#         print("detect 1 未检测到物体,存在未识别物体")
#         flag2, image2, rubbish_class2 = Detect(net, LABELS, COLORS,image_path)
#         if flag2:
#             pv.showText()
#             if rubbish_class2 != 5:
#                 SendMessage(rubbish_class2)
#             time.sleep(5)
#         else:
#             SendMessage(4)
#             print("detect 2 未检测到物体,存在未识别物体，假设其他垃圾")
#             time.sleep(5)
#     take_detect()


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
    flag, rubbish_class = Detect(net, LABELS, COLORS, image_path)
    if flag:
        time_num = 0
        pv.showText()
        if rubbish_class != 5:
            SendMessage(rubbish_class)
        # global photo_count
        # # cv2.imshow("img", image)
        # cv2.imwrite('../pic/' + 'detect1' + str(photo_count) + ".jpg", image)
        # photo_count += 1
        # time.sleep(5)
    else:
        add_num()
        # time.sleep(1)
    take_detect()



Detor = detector_config_for_All()
net = cv2.dnn.readNetFromDarknet(Detor.configPath, Detor.weightsPath)
LABELS = open(Detor.labelsPath).read().strip().split("\n")

Detor2 = detector_config_just_blank()
net2 = cv2.dnn.readNetFromDarknet(Detor2.configPath, Detor2.weightsPath)
LABELS2 = open(Detor2.labelsPath).read().strip().split("\n")

Detor3 = detector_config_for_Bottle()
net3 = cv2.dnn.readNetFromDarknet(Detor3.configPath, Detor3.weightsPath)
LABELS3 = open(Detor3.labelsPath).read().strip().split("\n")

COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")  # 随机生成颜色框


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
