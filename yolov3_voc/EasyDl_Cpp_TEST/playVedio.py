from tkinter import scrolledtext
import pygame
import time
import tkinter as tk
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import cv2
from PIL import Image, ImageTk
import tkinter.font as tf
import threading
from concurrent.futures import ThreadPoolExecutor
from imutils.video import WebcamVideoStream
import traceback
import os
import logger_print as log
class _text3:
    def __init__(self):
        self.count = 0
        self.line_text = []


class all_text:
    def __init__(self):
        # 垃圾投放次数
        self.COUNT = 0
        # 当前垃圾种类
        self.CATEGOARY = []
        # 垃圾满载检测标志
        self.FULL_LOAD_FLAG = False
        # 垃圾具体名称
        self.NAME = []
        self.NUMS = []


# 满载检测各类垃圾数量
class numOfRubbishCan:
    def __init__(self):
        # 有害垃圾
        self.harmfulBin = 0
        # 可回收垃圾
        self.recyclabelsBin = 0
        # 其他垃圾
        self.otherBin = 0
        # 厨余垃圾
        self.kinchenBin = 0

log_info = log.logger.info

# 主要文本
Main_text = all_text()
numberofRubbish = numOfRubbishCan()
_Text3 = _text3()

global photo
record_time = 0
video_times = 0

# # 图像转换，用于在画布中显示
# def tkImage(vc):
#     global video_times
#     frame = vc.read()
#     if(frame is None):
#         video_times +=1
#         return False
#     cvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     pilImage = Image.fromarray(cvimage)  # 转换成图片
#     pilImage = pilImage.resize((450, 320), Image.ANTIALIAS)
#     tkImage = ImageTk.PhotoImage(image=pilImage)
#     return tkImage


# # 图像的显示与更新
# def video():
#     vc1 = WebcamVideoStream(src='/home/ubuntu/python_pro/A_polyp/垃圾分类宣传1.mp4').start()
#     # vc1 = cv2.VideoCapture('../垃圾分类宣传2.mp4')
#     canvas1_create_image = canvas1.create_image
#     win_update_idletasks = win.update_idletasks
#     win_update = win.update
#     video_temp = []
#     def video_loop():
#         try:
#             global video_times
#             video_temp_append = video_temp.append
#             i = 0
#             while True:
#                 if(video_times == 0):
#                     img = tkImage(vc1)  # play speed adjust source of WebcamVideoStream
#                     if(img is False):
#                         continue
#                     else:
#                         video_temp_append(img)

#                 else:
#                     len_video = len(video_temp)
#                     if(i >= len_video -1):
#                         i = 0
#                     img = video_temp[i]
#                     i+=1
#                     time.sleep(0.16)
#                 canvas1_create_image(0, 0, anchor='nw', image=img)
#                 obr = img  # 重要语句，避免屏闪
#                 win_update_idletasks()  # 最重要的更新是靠这两句来实现
#                 win_update()
#         except:
#             traceback.print_exc()

#     video_loop()
#     vc1.stop()
#     cv2.destroyAllWindows()


def Show_Detect_Pic(show_detect_pic_Flag=False):
    global photo
    if(show_detect_pic_Flag):
        img_ori = Image.open("pic_save/laji.jpg.result-cpp.jpg")
        img_ori = img_ori.resize((450,320),Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img_ori)
        tk.Label(win,image=photo).place(x=5,y=550)


def receive():
    pass


def label_forget(text1):
    # label.grid_forget()
    text1.delete('0.0', tk.END)
    win.after(1000, showText)


# global i
# i = 0
def showText():
    showText2()
    showText3()
    global Main_text
    text_num = Main_text.COUNT
    text_categary = Main_text.NAME
    text_extr_categary = Main_text.CATEGOARY
    text_detect_num = Main_text.NUMS
    # if text_num is 2:
    #     text1.delete('1.0', tk.END)
    # text2.grid(row=0, column=2, padx=10, pady=10)
    global record_time
    text1_insert = text1.insert
    if record_time < text_num and text_num > 0:
        for i in range(len(text_categary)):
            # print(text_categary[i])
            # print(text_detect_num[i])
            # print(text_extr_categary[i])
            text_all = str(text_num) + " " + text_categary[i] + " {}".format(text_detect_num[i]) + " OK! "+text_extr_categary[i]
            text1_insert(tk.INSERT, text_all)
            text1_insert(tk.INSERT, '\n')
        record_time = text_num

    win.after(1000, showText)  # loop sentence

    # win.mainloop()

def showText3():
    text3.delete('0.0', tk.END)
    text3_insert = text3.insert
    text = "***NO.{}***\n".format(_Text3.count)
    text3_insert(tk.INSERT, text)
    text3_insert(tk.INSERT, '\n')
    for i in range(len(_Text3.line_text)):
        text3_insert(tk.INSERT,_Text3.line_text[i])
        text3_insert(tk.INSERT, '\n')

def showText2():
    text2.delete('0.0', tk.END)
    # flag = ''
    # if Main_text.FULL_LOAD_FLAG is True:
    #     flag = '已满载'
    # else:
    #     flag = '未满载'
    ft = tf.Font(family='微软雅黑', size=15)  # 设置初始字体
    a = '1.0'
    text2.tag_add('tag', a)
    text2.tag_config('tag', foreground='red', font=ft)

    a2 = '2.0'
    a3 = '3.0'
    a4 = '4.0'
    text2.tag_add('tag2', a)
    text2.tag_config('tag2', foreground='black', font=ft)

    flag1 = '未满载'
    flag2 = '未满载'
    flag3 = '未满载'
    flag4 = '未满载'
    text2_insert = text2.insert
    if numberofRubbish.kinchenBin >= 5:
        flag1 = '已满载'
        text2_insert(a, '厨余垃圾' + '、' + str(numberofRubbish.kinchenBin) + '，' + flag1 + '\n', 'tag')
    else:
        text2_insert(a, '厨余垃圾' + '、' + str(numberofRubbish.kinchenBin) + '，' + flag1 + '\n', 'tag2')

    if numberofRubbish.recyclabelsBin >= 5:
        flag2 = '已满载'
        text2_insert(a2, '可回收垃圾' + '、' + str(numberofRubbish.recyclabelsBin) + '，' + flag2 + '\n', 'tag')
    else:
        text2_insert(a2, '可回收垃圾' + '、' + str(numberofRubbish.recyclabelsBin) + '，' + flag2 + '\n', 'tag2')

    if numberofRubbish.harmfulBin >= 3:
        flag3 = '已满载'
        text2_insert(a3, '有害垃圾' + '、' + str(numberofRubbish.harmfulBin) + '，' + flag3 + '\n', 'tag')
    else:
        text2_insert(a3, '有害垃圾' + '、' + str(numberofRubbish.harmfulBin) + '，' + flag3 + '\n', 'tag2')

    if numberofRubbish.otherBin >= 5:
        flag4 = '已满载'
        text2_insert(a4, '其他垃圾' + '、' + str(numberofRubbish.otherBin) + '，' + flag4 + '\n', 'tag')
    else:
        text2_insert(a4, '其他垃圾' + '、' + str(numberofRubbish.otherBin) + '，' + flag4 + '\n', 'tag2')



def playSound():

    pygame.init()
    pygame.mixer.init()
    music_conf = pygame.mixer.music
    music = music_conf.load("/home/ubuntu/python_pro/A_polyp/垃圾分类宣传2.wav")
    while True:
        if music_conf.get_busy() == False:
            music_conf.play()


def playvedio():
    # while 1:
    # video()
    while True:
        try:
            mes = os.popen("cd /home/ubuntu/python_pro/A_polyp/yolov3_voc/EasyDl_Cpp_TEST/CPP_File/build && ./Image_Test_01")
            mes = mes.read()
            log_info("play Video!")
        except Exception as e:
            log_info(e)



'''布局'''
win = tk.Tk()
win.geometry("550x1000+1255+0")
# canvas1 = Canvas(win, bg='white', width=450, height=320)
# canvas1.place(x=5,y=550)
text1 = scrolledtext.ScrolledText(win, width=27, height=20, font=('Times', 15, 'bold')) # mark ,添加可显示垃圾类型宽度
text1.grid(row=1, column=1)  # text1  place in (0,1)



text2 = tk.Text(win, width=27, height=11, font=('Times', 15, 'bold'))
# text2.grid(row=0, column=2)
text2.grid(row=1, column=2)

text3 = tk.Text(win, width=27, height=10, font=('Times', 15, 'bold'))
text3.grid(row=2, column=1)

# win_text = tk.Text(win, width=20, height=1,font=('Times',15,'bold'))  # 任务完成提示框,调整边框大小位置
# win_text.grid(row=1, column=2)
# win_text.insert("insert","满载检测： ")
# label = tk.Label(win,text="hellowtf",height=3,width=100,bg='white')
# label.pack()

# showText()


if __name__ == '__main__':
    p1 = threading.Thread(target=playvedio)
    # p1.setDaemon(True)
    p1.start()
    p2 = threading.Thread(target=showText)
    # p2.setDaemon(True)
    p2.start()
    # p3 = threading.Thread(target=playSound)
    # p3.setDaemon(True)
    # p3.start()
    win.mainloop()
