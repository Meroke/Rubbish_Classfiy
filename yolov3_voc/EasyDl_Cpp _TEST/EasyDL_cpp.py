import os
import time
import rubbish_class as RBCls
# import playVedio as pv

# fixed save position of Pic
# path =  "/home/ubuntu/python_pro/A_polyp/pic_save/laji.jpg"
path = "/home/ubuntu/python_pro/A_polyp/pic_save/laji.jpg"
# path = "/home/ubuntu/Pictures/"
temp_num = 0
def Easydl_Cpp():
    # init
    rubbish_class=0
    flag = False
    # path = '/home/ubuntu/Pictures/1.jpeg'
    global path, temp_num
    # path = path + "{}.png".format(temp_num)
    # temp_num += 1
    task = 'cd /home/ubuntu/Develop_Tool/EasyEdge_speed/cpp/baidu_easyedge_linux_cpp_aarch64/src/build/demo_image_inference/ && ./easyedge_image_inference /home/ubuntu/Develop_Tool/EasyEdge_speed/RES {}'.format(
        path)
    text = os.popen(task)
    text = text.read()
    target = []
    line = text.split('\n')

    name = []
    confidence = []
    # every line like: 6, battary, p:0.999548, coordinate: 0.1209, 0.600641, 0.262635, 0.882932
    if len(line) > 3:
        # print(line)
        num = line[0].split(':')[1]
        for i in range(1,int(num)+1):
            target.append(line[i])
            # print(line[i])
            temp_confidence = line[i].split(',')[2].split(':')[1].strip()
            if float(temp_confidence) > 0.8:
                temp_name = line[i].split(',')[1].strip()
                name.append(temp_name)
                confidence.append(temp_confidence)

        # actically, the tow lists of name and confidence, get all targets in this frame,
        # But it's useless for this machine that not equipped movable grab structure
        if(len(confidence) > 0):
            flag = True
            _max_conf = confidence.index(max(confidence))
            print("Main:\nBest target:{}".format(name[_max_conf],confidence[_max_conf]))
            rubbish_class = RBCls.return_rubbish_class(name[_max_conf])
            print("Send Class:{}".format(rubbish_class))
            # unrecorded rubbish is Other Rubbish
            if rubbish_class != 5:  # 不是白板
                if rubbish_class != 1 and rubbish_class != 2 and rubbish_class != 3:  # 不在记录中的垃圾全部识别为其他垃圾
                    rubbish_class = 4
            # pv.Main_text.NAME = RBCls.ChineseName[name[_max_conf]]
        print("Detection List:------------")
        for i in range(len(confidence)):
            print(name[i],confidence[i])
        print("END-------------")
        return flag, rubbish_class

if __name__ == '__main__':
    Easydl_Cpp()