# 1:厨余垃圾，2：有害垃圾，3：可回收垃圾，4:其他垃圾
rubbish = {'apple': 1, 'orange': 1, 'pear': 1, 'broccoli': 1, 'carrot': 1, 'potato': 1, 'blackBanana': 1, \
           'banana': 1, 'banana_peel': 1, 'garlic': 1, 'grape': 1, 'singlegrape': 1, 'green': 1, 'tomato': 1,\
           'cucumber': 1,\
           'pea': 1, 'multpea': 1, 'onion': 1, 'whiteradish': 1, 'hmg': 1, 'longyan': 1, 'mongo': 1, 'oil_orange': 1,\
           'baicai': 1, \
           'can': 3, 'can_end': 3, 'bottle': 3,'bottle_label': 3, \
           'battary': 2, 'battery_end': 2,'battery5': 2, \
           'cigarette': 4, \
           'blank': 5}


ChineseName = {'apple': '苹果', 'orange': '橘子', 'pear': '梨', 'broccoli': '西兰花', 'carrot': '萝卜', 'potato': '土豆',\
               'blackBanana': '香蕉', \
               'banana': '香蕉', 'banana_peel': '香蕉', 'garlic': '大蒜', 'grape': '葡萄', 'singlegrape': '葡萄', 'green': '青菜',\
               'tomato': '番茄', 'cucumber': '黄瓜', \
               'pea': '豌豆', 'multpea': '豌豆', 'onion': '洋葱', 'hmg': '哈密瓜', 'whiteradish': '萝卜', 'longyan': '龙眼',\
               'mongo': '芒果', 'oil_orange': '橘子', 'baicai': '白菜', \
               'can': '易拉罐', 'can_end': '易拉罐', 'bottle': '瓶子', 'bottle_label':'瓶子',\
               'battary': '电池', 'battery_end': '电池','battery5':'电池' ,\
               'cigarette': '香烟', \
               'blank': '白板'}

rubbish_class=0
def return_rubbish_class(class_name):
    key = class_name
    if rubbish.get(key) is not None:
        return rubbish[key]
    else:
        return 0

