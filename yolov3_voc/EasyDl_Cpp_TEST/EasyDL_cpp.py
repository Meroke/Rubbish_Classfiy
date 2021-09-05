import os
import time
import rubbish_class as RBCls
import playVedio as pv
import logger_print as log
import math
from collections import Counter
# fixed save position of Pic
# path =  "/home/ubuntu/python_pro/A_polyp/pic_save/laji.jpg"
path = "/home/ubuntu/python_pro/A_polyp/pic_save/laji.jpg"
# path = "/home/ubuntu/Pictures/"
temp_num = 0
log_info = log.logger.info

def Final_Check_List_Log(confidence,name):
    log_info("Final Check List:------------")
    pv._Text3.line_text.clear()
    for i in range(len(confidence)):
        text =name[i] + str(confidence[i])
        log_info(text)
        pv._Text3.line_text.append(text)
    log_info("END-------------")

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
                    log_info( '(' + list_coordinate[i][k] + ',' + list_coordinate[i][k+1]+ ') ' \
                        '(' + list_coordinate[j][k] + ',' + list_coordinate[j][k+1] + ')' + ' dis: '+ str(dis))
                    log_info(str(k)+ ' n:' + name[i] + ' p:' + confidence[i] + ' ' + list_coordinate[i][k] \
                        + ' n:' + name[j] + ' p:'+ confidence[j] + ' ' + list_coordinate[j][k])
                    if(same_count > 1):
                        if(confidence[i] > confidence[j]):
                            delete_index = j
                        else:
                            delete_index = i
                        confidence.pop(delete_index)
                        name.pop(delete_index)


def Check_repeat(name,confidence,name_copy):
    i= 0
    j = i+1
    lens = len(name)
    # do not use for ... in ...
    while(i < lens):
        while(j < lens):
            if(name[i] == name [j]):
                name.pop(j)
                confidence.pop(j)
                j -= 1
                lens -= 1
            j+= 1
        i += 1

    name_nums = []
    name_nums_append = name_nums.append
    for num in range(len(name)):
        name_nums_append(name_copy.count(name[num]))
    return name_nums

def Add_Message(rubbish_class,name_nums,mode):
    if(mode != 0) :
        pv._Text3.count += 1
        pv_Main_Text = pv.Main_text
        pv_Main_CATEGORY =pv_Main_Text.CATEGOARY
        pv_numberofRubbish = pv.numberofRubbish
        if (len(rubbish_class) > 0):
            pv_Main_Text.COUNT += 1
            pv_Main_CATEGORY.clear()
            for i in range(len(rubbish_class)):
                if(rubbish_class[i] > 0 and rubbish_class[i] < 5):
                    # print("send:: {}".format(rubbish_class))
                    # log_info("send:: {}".format(rubbish_class))
                    if rubbish_class[i] is 1:
                        pv_Main_CATEGORY.append("厨余垃圾")
                        pv_numberofRubbish.kinchenBin += name_nums[i]
                    elif rubbish_class[i] is 2:
                        pv_Main_CATEGORY.append("有害垃圾")
                        pv_numberofRubbish.harmfulBin += name_nums[i]
                    elif rubbish_class[i] is 3:
                        pv_Main_CATEGORY.append("可回收垃圾")
                        pv_numberofRubbish.recyclabelsBin += name_nums[i]
                    elif rubbish_class[i] is 4:
                        pv_Main_CATEGORY.append("其他垃圾")
                        pv_numberofRubbish.otherBin += name_nums[i]


def Easydl_Cpp(mode=1):
    # init
    rubbish_class=[]
    flag = False
    # path = '/home/ubuntu/Pictures/1.jpeg'
    global path, temp_num
    if(mode == 0):
        # warnup  pic
        path = "/home/ubuntu/Pictures/7.png"
    else:
        path = "/home/ubuntu/python_pro/A_polyp/pic_save/laji.jpg"

    log_info("\n*****NO.{} Detection******".format(temp_num))
    # path = path + "{}.png".format(temp_num)
    # temp_num += 1
    # print("detect file in:"+ path)
    log_info("detect file in:"+ path)
    task = 'cd /home/ubuntu/Develop_Tool/EasyEdge_speed_v7/cpp/baidu_easyedge_linux_cpp_aarch64/src/build/demo_image_inference/ && ./easyedge_image_inference /home/ubuntu/Develop_Tool/EasyEdge_speed_v7/RES {}'.format(
        path)
    text = os.popen(task)
    text = text.read()
    target = []
    line = text.split('\n')

    name = []
    name_append = name.append
    confidence = []
    confidence_append = confidence.append
    list_coordinate=[]
    list_coordinate_append = list_coordinate.append
    _max_conf = 0
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
                line_split = line[i].split(',')
                # cooridinate
                temp_list_append = temp_list.append
                temp_list_append(line_split[3].split(':')[1])
                temp_list_append(line_split[4])
                temp_list_append(line_split[5])
                temp_list_append(line_split[6])
                list_coordinate_append(temp_list)
                # name
                temp_name = line_split[1].strip()
                name_append(temp_name)
                # confidence
                confidence_append(temp_confidence)

        # actically, the tow lists of name and confidence, get all targets in this frame,
        # But it's useless for this machine that not equipped movable grab structure
        if(len(confidence) > 0):

            Final_Check_List(list_coordinate,confidence,name)
            Final_Check_List_Log(confidence,name)
            
            name_copy = name.copy()
            name_nums = Check_repeat(name,confidence,name_copy)
            pv.Main_text.NUMS = name_nums

            flag = True
            _max_conf = confidence.index(max(confidence))
            log_info("Main:\nBest target:{}".format(name[_max_conf],confidence[_max_conf]))
            if(len(pv.Main_text.NAME) > 0):
                pv.Main_text.NAME =[]
                
                # pv.Main_text.NAME.clear()
            for i in range(len(confidence)):
                pv.Main_text.NAME.append(RBCls.ChineseName[name[i]])
                rubbish_class.append(RBCls.return_rubbish_class(name[i]))

            log_info("Record Class:{}".format(rubbish_class[_max_conf]))

            Add_Message(rubbish_class,name_nums,mode)

    if(mode == 1):
        save_path = "pic_save/laji.jpg.result-cpp.jpg"
        if(os.path.exists(save_path)):
            pv.Show_Detect_Pic(True)
            os.popen("mv pic_save/laji.jpg.result-cpp.jpg pic/laji{}.jpg".format(temp_num))
        else:
            log.logger.error("no found result.jpg!")

    temp_num += 1

    return flag, rubbish_class,_max_conf

if __name__ == '__main__':
    Easydl_Cpp()