import numpy as np
import cv2
import time
import os
import threading
# import EasyDL_detect as ea
import EasyDL_cpp as ec
import playVedio as pv
import commication as COM



if __name__ == "__main__":
    print("启动等待2s")
    time.sleep(2)
    p1 = threading.Thread(target=pv.playvedio)
    # p1.setDaemon(True)
    p1.start()
    p2 = threading.Thread(target=COM.pylisten,args=(COM.my_serial,))
    p2.start()

    p4 = threading.Thread(target=pv.playSound)
    # p4.setDaemon(True)
    p4.start()

    # p5 = threading.Thread(target=recvMessage)
    # p5.start()

    pv.win.mainloop()
    # while 1:
    #     open_sign()
