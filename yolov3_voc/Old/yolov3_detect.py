import cv2
import numpy as np
import cv2
import time
import os
import threading



class detector_config_for_All:
    def __init__(self):
        self.weightsPath = '../weights_blank/my-v3_515000.weights'  # 模型权重文件
        self.configPath = "../weights_blank/my-v3.cfg"  # 模型配置文件
        self.labelsPath = "../weights_blank/classes.names"  # 模型类别标签文件

Detor = detector_config_for_All()
net = cv2.dnn.readNetFromDarknet(Detor.configPath, Detor.weightsPath)
LABELS = open(Detor.labelsPath).read().strip().split("\n")
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")  # 随机生成颜色框
# 全局数值初始化
list_num = 0
photo_count = 0
boxes = []
confidences = []
classIDs = []
time_num = 0
def Detect(net,LABELS,COLORS,image_path) -> object:
    # 返回值 初始化
    detect_flag = 0
    rubbish_class= 0

    # global p3
    # 初始化一些参数

    # 加载 网络配置与训练的权重文件 构建网络
    # ser = serial.Serial("/dev/ttyACM0", 9600, timeout=1) # mark
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
            for seq in box_seq:
                (x, y) = (boxes[seq][0], boxes[seq][1])  # 框左上角
                (w, h) = (boxes[seq][2], boxes[seq][3])  # 框宽高
                color = COLORS[classIDs[seq]].tolist()
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 1)  # 画框
                text = "{}: {:.4f}".format(LABELS[classIDs[seq]], confidences[seq])
                print("======" + str(text) + "======")
                # 获取垃圾具体中文名称
                # 在图像上标注垃圾种类
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_DUPLEX, 1, color, 1)  # 写字
                detect_flag = 1

    except AttributeError:
        print("识别失败－－－－－－－－－－－－－－")

    global photo_count
    # cv2.imshow("img", image)
    cv2.imwrite('../pic/' + 'detect1' + str(photo_count) + ".jpg", image)
    photo_count += 1

    # cv2.waitKey(0)
    cv2.destroyAllWindows()
    time.sleep(2)

    return detect_flag, image, rubbish_class

if __name__ == "__main__":
    image_path = '../pic_bottle/detect/4.jpg'
    flag, image, rubbish_class = Detect(net,LABELS,COLORS,image_path)
    # cv2.imshow("img", image)
    cv2.imwrite('../pic_bottle/detect/' + 'detect1.jpg', image)