import os
import time
import rubbish_class as RBCls
import math
# import playVedio as pv

# fixed save position of Pic
# path =  "/home/ubuntu/python_pro/A_polyp/pic_save/laji.jpg"
# path = "/home/ubuntu/python_pro/A_polyp/pic_save/laji.jpg"
# path = "/home/ubuntu/Pictures/"
temp_num = 0
conf_num_sum=0
conf_sum = 0

# do not stright copy. some part has benn notes,like pv..
def Easydl_Cpp(path):
    # init
    global conf_num_sum, conf_sum
    rubbish_class=0
    flag = False
    # path = '/home/ubuntu/Pictures/1.jpeg'
    global temp_num
    # path = path + "{}.png".format(temp_num)
    # temp_num += 1
    # task = 'cd /home/ubuntu/Develop_Tool/EasyEdge_speed_v3_super/cpp/baidu_easyedge_linux_cpp_aarch64/src/build/demo_image_inference/ && ./easyedge_image_inference /home/ubuntu/Develop_Tool/EasyEdge_speed_v3_super/RES {}'.format(
    #     path)

    task = "cd /home/ubuntu/Develop_Tool/EasyEdge_speed_v7/cpp/baidu_easyedge_linux_cpp_aarch64/src/build/demo_image_inference&& ./easyedge_image_inference /home/ubuntu/Develop_Tool/EasyEdge_speed_v7/RES {}".format(path)
    text = os.popen(task)
    text = text.read()
    target = []
    line = text.split('\n')

    name = []
    confidence = []
    list_coordinate=[]
    # every line like: 6, battary, p:0.999548, coordinate: 0.1209, 0.600641, 0.262635, 0.882932
    if len(line) > 3:
        print(line)
        # num = line[0].split(':')[1] # actual num of detection
        # the start num maybe 2 or 1. It's depends on the demo has writen machine License!!
        for i in range(1,len(line)-3):
            target.append(line[i])
            print(line[i])
            temp_list = []
            temp_confidence = line[i].split(',')[2].split(':')[1].strip()

            # the demo has another confidence limiter(also 0.80) !!
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
                conf_sum += float(temp_confidence)
                conf_num_sum += 1

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
                        print((list_coordinate[i][k],list_coordinate[i][k+1]),\
                            (list_coordinate[j][k],list_coordinate[j][k+1]),dis)
                        print(k,name[i],confidence[i],list_coordinate[i][k], name[j],confidence[j],list_coordinate[j][k])
                        if(same_count > 1):
                            if(confidence[i] > confidence[j]):
                                delete_index = j
                            else:
                                delete_index = i
                            confidence.pop(delete_index)
                            name.pop(delete_index)

        print("Final Check List:------------")
        for i in range(len(confidence)):
            print(name[i],confidence[i])
        print("END-------------")        
        return flag, rubbish_class

# result:
# v1: 100
# cost time: 123.04480648040771s
# cost aver: 1.2304480648040772s
# detect num:322
# confidence_aver: 0.9902121086956518

# v2: 100
# cost time: 122.11560940742493s
# cost aver: 1.2211560940742492s
# detect num:326
# confidence_aver: 0.988185981595092

# v3_super  10
# cost time: 178.07603645324707s
# cost aver: 17.807603645324708s
# detect num:29
# confidence_aver: 0.9776870000000003

# v7_super 100
# cost time: 199.9807505607605s
# cost aver: 1.999807505607605s
# detect num:293
# confidence_aver: 0.9639292286689418
if __name__ == '__main__':
    start_time = time.time()
    floader_path = "/home/ubuntu/Pictures/test"
    list_file = os.listdir(floader_path)
    # num = 0
    for i in list_file:
        file = os.path.join(floader_path,i)
        Easydl_Cpp(file)
        # num += 1
        # if(num == 9):
        #     break

    end_time = time.time()
    cost = end_time - start_time
    print("cost time: "+str(cost) + "s")
    print("cost aver: "  +str(cost / 100) + "s")
    print("detect num:"+ str(conf_num_sum))
    print("confidence_aver: " + str(conf_sum / conf_num_sum))