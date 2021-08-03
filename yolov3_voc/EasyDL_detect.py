
"""
EasyDL 图像分类 调用模型公有云API Python3实现
"""

import json
import base64
import requests
import cv2
import playVedio as pv
import serial

"""
使用 requests 库发送请求
使用 pip（或者 pip3）检查我的 python3 环境是否安装了该库，执行命令
  pip freeze | grep requests
若返回值为空，则安装该库
  pip install requests
"""

# 串口初始化
# port = "/dev/rfcomm2"
port = "/dev/rfcomm3"
ser = serial.Serial(port, 9600)
# 目标图片的 本地文件路径，支持jpg/png/bmp格式
IMAGE_FILEPATH = "../pic_save/laji.jpg"
nums = 0


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


def return_rubbish_class(class_name):
    key = class_name
    if key in rubbish:
        return rubbish[key]
    else:
        return 0


def detectEasyDL():
    global IMAGE_FILEPATH
    flag = 0
    image = cv2.imread(IMAGE_FILEPATH)
    rubbish_name =""
    print("start-------------")
    # 可选的请求参数
    # top_num: 返回的分类数量，不声明的话默认为 6 个
    PARAMS = {"top_num": 2}

    # 服务详情 中的 接口地址
    #MODEL_API_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/detection/part_classfiy"
    MODEL_API_URL ="https://aip.baidubce.com/rpc/2.0/ai_custom/v1/detection/ORI_CLAS"
    # 调用 API 需要 ACCESS_TOKEN。若已有 ACCESS_TOKEN 则于下方填入该字符串
    # 否则，留空 ACCESS_TOKEN，于下方填入 该模型部署的 API_KEY 以及 SECRET_KEY，会自动申请并显示新 ACCESS_TOKEN
    ACCESS_TOKEN = "24.6aee38519afc0a5ceb2b47f570d45b61.2592000.1630216382.282335-24627689"
    #ACCESS_TOKEN = ""
    API_KEY = "RRT6KnVYGQWMNfpiuaabOanQ"
    SECRET_KEY = "qOFcYSvnYSaPygGrId76d5a8hHT9pYGm"

    print("1. 读取目标图片 '{}'".format(IMAGE_FILEPATH))
    with open(IMAGE_FILEPATH, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        base64_str = base64_data.decode('UTF8')
    print("将 BASE64 编码后图片的字符串填入 PARAMS 的 'image' 字段")
    PARAMS["image"] = base64_str


    if not ACCESS_TOKEN:
        print("2. ACCESS_TOKEN 为空，调用鉴权接口获取TOKEN")
        auth_url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials"\
                   "&client_id={}&client_secret={}".format(API_KEY, SECRET_KEY)
        auth_resp = requests.get(auth_url)
        auth_resp_json = auth_resp.json()
        ACCESS_TOKEN = auth_resp_json["access_token"]
        print("新 ACCESS_TOKEN: {}".format(ACCESS_TOKEN))
    else:
        print("2. 使用已有 ACCESS_TOKEN")

    print("3. 向模型接口 'MODEL_API_URL' 发送请求")
    request_url = "{}?access_token={}".format(MODEL_API_URL, ACCESS_TOKEN)
    response = requests.post(url=request_url, json=PARAMS)
    response_json = response.json()
    response_str = json.dumps(response_json, indent=4, ensure_ascii=False) # indent:4格缩进
    # print("结果:{}".format(response_str))

    res_load = json.loads(response_str)
    if(len(res_load['results']) > 0):
        print(len(res_load['results']))
        global nums
        for i in range(len(res_load['results'])):
            h = res_load['results'][i]['location']['height']
            x = res_load['results'][i]['location']['left']
            w = res_load['results'][i]['location']['width']
            y = res_load['results'][i]['location']['top']
            cv2.rectangle(image, (x, y), (x + w, y + h), 255, 5)  # 画框
            rubbish_name = res_load['results'][i]['name']
            text = rubbish_name + " " + str(res_load['results'][i]['score'])
            cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_TRIPLEX, 3, 125, 2)  # 写字

            rubbish_class = return_rubbish_class(rubbish_name)
            if rubbish_class != 5:  # 不是白板
                if rubbish_class != 1 and rubbish_class != 2 and rubbish_class != 3:  # 不在记录中的垃圾全部识别为其他垃圾
                    rubbish_class = 4

            pv.Main_text.NAME = ChineseName[rubbish_name]

        # cv2.resize(image, (512, 512))
        # cv2.imshow('img', image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        cv2.imwrite('../pic/{}.jpg'.format(nums), image)
        nums += 1
        flag = True
    return flag, rubbish_class
# print(res_load['results'][0])

if __name__  == "__main__":
    pic_path = "/home/meroke/Python_pro/python_tool/index.jpeg"
    name = detectEasyDL(pic_path)