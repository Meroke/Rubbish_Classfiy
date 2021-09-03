import pygame
import time
import tkinter as tk
from tkinter import *
import cv2
from PIL import Image, ImageTk
import tkinter.font as tf
import threading
from concurrent.futures import ThreadPoolExecutor
from imutils.video import WebcamVideoStream
import traceback

class _text3:
    def __init__(self):
        self.count = 0
        self.line_text = []


class all_text:
    def __init__(self):
        # 垃圾投放次数
        self.COUNT = 0
        # 当前垃圾种类
        self.CATEGOARY = "NONE"
        # 垃圾满载检测标志
        self.FULL_LOAD_FLAG = False
        # 垃圾具体名称
        self.NAME = ''


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


# 主要文本
Main_text = all_text()
numberofRubbish = numOfRubbishCan()
_Text3 = _text3()

record_time = 0
window_width = 1850
window_height = 1000
image_width = int(window_width)
image_height = int(window_height)
imagepos_x = 0
imagepos_y = 0
butpos_x = 450
butpos_y = 450


# vc1 = cv2.VideoCapture('垃圾分类.flv')  # 读取视频
# vc1 = cv2.VideoCapture('D:/test.flv')


# 图像转换，用于在画布中显示
def tkImage(vc):
    frame = vc.read()
    cvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pilImage = Image.fromarray(cvimage)  # 转换成图片
    pilImage = pilImage.resize((image_width, image_height), Image.ANTIALIAS)
    tkImage = ImageTk.PhotoImage(image=pilImage)
    return tkImage


# 图像的显示与更新
def video():
    vc1 = WebcamVideoStream(src='/home/ubuntu/python_pro/A_polyp/垃圾分类宣传2.mp4').start()
    # vc1 = cv2.VideoCapture('../垃圾分类宣传2.mp4')
    def video_loop():
        try:
            while True:
                img = tkImage(vc1)  # play speed adjust source of WebcamVideoStream
                canvas1.create_image(0, 0, anchor='nw', image=img)
                obr = img  # 重要语句，避免屏闪
                win.update_idletasks()  # 最重要的更新是靠这两句来实现
                win.update()
        except:
            traceback.print_exc()

    video_loop()
    vc1.stop()
    cv2.destroyAllWindows()


def receive():
    pass


def label_forget(text1):
    # label.grid_forget()
    text1.delete('0.0', tk.END)
    win.after(1000, showText)


# def task_label_init():
#     win_text.insert("insert","满载检测： ")
#     win.after(3000, label_forget)


# global i
# i = 0
def showText():
    showText2()
    showText3()
    global Main_text
    text_num = Main_text.COUNT
    text_categary = Main_text.NAME
    text_extr_categary = Main_text.CATEGOARY
    # if text_num is 2:
    #     text1.delete('1.0', tk.END)
    # text2.grid(row=0, column=2, padx=10, pady=10)
    global record_time
    if record_time < text_num and text_num > 0:
        text_all = str(text_num) + " " + text_categary + " 1" + " OK! "+text_extr_categary;
        text1.insert(tk.INSERT, text_all)
        text1.insert(tk.INSERT, '\n')
        record_time = text_num
    # text2.insert(tk.INSERT,text_categary)
    # task_label_init()
    #  time.sleep(2)
    # label_forget(text1)
    # win.after(1000, label_forget, text1)

    win.after(1000, showText)  # loop sentence

    # win.mainloop()

def showText3():
    text3.delete('0.0', tk.END)
    text = "***NO.{}***\n".format(_Text3.count)
    text3.insert(tk.INSERT, text)
    text3.insert(tk.INSERT, '\n')
    for i in range(len(_Text3.line_text)):
        text3.insert(tk.INSERT,_Text3.line_text[i])
        text3.insert(tk.INSERT, '\n')

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

    if numberofRubbish.kinchenBin >= 5:
        flag1 = '已满载'
        text2.insert(a, '厨余垃圾' + '、' + str(numberofRubbish.kinchenBin) + '，' + flag1 + '\n', 'tag')
    else:
        text2.insert(a, '厨余垃圾' + '、' + str(numberofRubbish.kinchenBin) + '，' + flag1 + '\n', 'tag2')

    if numberofRubbish.recyclabelsBin >= 5:
        flag2 = '已满载'
        text2.insert(a2, '可回收垃圾' + '、' + str(numberofRubbish.recyclabelsBin) + '，' + flag2 + '\n', 'tag')
    else:
        text2.insert(a2, '可回收垃圾' + '、' + str(numberofRubbish.recyclabelsBin) + '，' + flag2 + '\n', 'tag2')

    if numberofRubbish.harmfulBin >= 3:
        flag3 = '已满载'
        text2.insert(a3, '有害垃圾' + '、' + str(numberofRubbish.harmfulBin) + '，' + flag3 + '\n', 'tag')
    else:
        text2.insert(a3, '有害垃圾' + '、' + str(numberofRubbish.harmfulBin) + '，' + flag3 + '\n', 'tag2')

    if numberofRubbish.otherBin >= 5:
        flag4 = '已满载'
        text2.insert(a4, '其他垃圾' + '、' + str(numberofRubbish.otherBin) + '，' + flag4 + '\n', 'tag')
    else:
        text2.insert(a4, '其他垃圾' + '、' + str(numberofRubbish.otherBin) + '，' + flag4 + '\n', 'tag2')



def playSound():
    # while 1:
    #     file = "/home/ubuntu/python_pro/A_polyp/垃圾分类宣传2.wav"
    #     pygame.mixer.init()
    #     print("播放音乐1")
    #     track = pygame.mixer.music.load(file)
    #     pygame.mixer.music.play()
    #     time.sleep(58)
    #     pygame.mixer.music.stop()
    pygame.init()
    pygame.mixer.init()
    music = pygame.mixer.music.load("/home/ubuntu/python_pro/A_polyp/垃圾分类宣传2.wav")
    while True:
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play()


def playvedio():
    while 1:
        video()


'''布局'''
win = tk.Tk()
win.geometry(str(window_width) + 'x' + str(window_height))
canvas1 = Canvas(win, bg='white', width=image_width, height=image_height)
canvas1.place(x=imagepos_x, y=imagepos_y)
text1 = tk.Text(win, width=27, height=21, font=('Times', 15, 'bold')) # mark ,添加可显示垃圾类型宽度
text1.grid(row=1, column=1)  # text1  place in (0,1)

text2 = tk.Text(win, width=22, height=11, font=('Times', 15, 'bold'))
# text2.grid(row=0, column=2)
text2.place(relx=0.93,rely=0.12,anchor=CENTER)

text3 = tk.Text(win, width=22, height=21, font=('Times', 15, 'bold'))
text3.place(x=1570,y=600)

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
    p3 = threading.Thread(target=playSound)
    # p3.setDaemon(True)
    p3.start()
    win.mainloop()
