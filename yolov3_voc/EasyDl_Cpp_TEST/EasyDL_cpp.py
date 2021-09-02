import os
import time
import rubbish_class as RBCls
import playVedio as pv
import logger_print as log
import math

# fixed save position of Pic
# path =  "/home/ubuntu/python_pro/A_polyp/pic_save/laji.jpg"
path = "/home/ubuntu/python_pro/A_polyp/pic_save/laji.jpg"
# path = "/home/ubuntu/Pictures/"
temp_num = 0

def Final_Check_List_Log(confidence,name):
    log.logger.info("Final Check List:------------")
    for i in range(len(confidence)):
        text =name[i] + str(confidence[i])
        log.logger.info(text)
    log.logger.info("END-------------")

def Final_Check_List(list_coordinate,confidence,name):
    # final check, delete error or excess recognization boxs 
    print(list_coordinate)
    for i in range(len(list_coordinate)-1):
        for j in range(i+1,len(list_coordinate)):
            same_count = 0
            for k in range(0,3,2):
                dis = math.sqrt(math.pow(float(list_coordinate[i][k]) - float(list_coordinate[j][k]),2) + \
                math.pow(float(list_coordinate[i][k+1]) - float(list_coordinate[j][k+1]),2))
                if(dis < 10):
                    same_count +=1
                    log.logger_coordinate.info( '(' + list_coordinate[i][k] + ',' + list_coordinate[i][k+1]+ ') ' \
                        '(' + list_coordinate[j][k] + ',' + list_coordinate[j][k+1] + ')' + ' dis: '+ str(dis))
                    log.logger_coordinate.info(str(k)+ ' n:' + name[i] + ' p:' + confidence[i] + ' ' + list_coordinate[i][k] \
                        + ' n:' + name[j] + ' p:'+ confidence[j] + ' ' + list_coordinate[j][k])
                    if(same_count > 1):
                        if(confidence[i] > confidence[j]):
                            delete_index = j
                        else:
                            delete_index = i
                        confidence.pop(delete_index)
                        name.pop(delete_index)

def Easydl_Cpp(mode=1):
    # init
    rubbish_class=0
    flag = False
    # path = '/home/ubuntu/Pictures/1.jpeg'
    global path, temp_num
    if(mode == 0):
        # warnup  pic
        path = "/home/ubuntu/Pictures/7.png"
    else:
        path = "/home/ubuntu/python_pro/A_polyp/pic_save/laji.jpg"
    # path = path + "{}.png".format(temp_num)
    # temp_num += 1
    # print("detect file in:"+ path)
    log.logger.info("detect file in:"+ path)
    task = 'cd /home/ubuntu/Develop_Tool/EasyEdge_speed_v2/cpp/baidu_easyedge_linux_cpp_aarch64/src/build/demo_image_inference/ && ./easyedge_image_inference /home/ubuntu/Develop_Tool/EasyEdge_speed/RES {}'.format(
        path)
    text = os.popen(task)
    text = text.read()
    target = []
    line = text.split('\n')

    name = []
    confidence = []
    list_coordinate=[]
    # every line like: 6, battary, p:0.999548, coordinate: 0.1209, 0.600641, 0.262635, 0.882932
    if len(line) > 3:
        # # print(line)
        num = line[0].split(':')[1]
        for i in range(1,len(line)-3):
            target.append(line[i])
            # # print(line[i])
            temp_list = []
            temp_confidence = line[i].split(',')[2].split(':')[1].strip()
            if float(temp_confidence) > 0.8:
                # cooridinate
                temp_list.append(line[i].split(',')[3].split(':')[1])
                temp_list.append(line[i].split(',')[4])
                temp_list.append(line[i].split(',')[5])
                temp_list.append(line[i].split(',')[6])
                list_coordinate.append(temp_list)
                # name
                temp_name = line[i].split(',')[1].strip()
                name.append(temp_name)
                # confidence
                confidence.append(temp_confidence)

        # actically, the tow lists of name and confidence, get all targets in this frame,
        # But it's useless for this machine that not equipped movable grab structure
        if(len(confidence) > 0):
            flag = True
            _max_conf = confidence.index(max(confidence))
            log.logger.info("Main:\nBest target:{}".format(name[_max_conf],confidence[_max_conf]))
            rubbish_class = RBCls.return_rubbish_class(name[_max_conf])
            log.logger.info("Record Class:{}".format(rubbish_class))

            pv.Main_text.NAME = RBCls.ChineseName[name[_max_conf]]
        log.logger.info("Detection List:------------")
        for i in range(len(confidence)):
            text =name[i] + str(confidence[i])
            log.logger.info(text)
        log.logger.info("END-------------")

        Final_Check_List(list_coordinate,confidence,name)
        Final_Check_List_Log(confidence,name)

    return flag, rubbish_class

if __name__ == '__main__':
    Easydl_Cpp()