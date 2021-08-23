import serial
import time
import platform


def serial_init():
    if 'Linux' in platform.platform():
        try:
            print("using USB0")
            com1 = serial.Serial(
                '/dev/ttyUSB0',
                # '/dev/ttyUSB2',

                115200,
                timeout=2,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE)
        except:
            print("using USB1")
            com1 = serial.Serial(
                '/dev/ttyUSB1',
                # '/dev/ttyUSB2',

                115200,
                timeout=2,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE)



    elif 'Windows' in platform.platform():
        com1 = serial.Serial(
            'COM60',
            115200,
            timeout=2,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE)

    else:
        raise RuntimeError('Unsupported platform.')

    time.sleep(1)
    wheel_com = com1

    return wheel_com

# ----------------------------------------------------------外圈开始

def go_forward(serial_wheel):
    pathw = '1F'
    serial_wheel.write(pathw.encode("utf-8"))
    print("go forward---------------------------------")
    while (True):
        if isComplete(serial_wheel) == True:
            break

def go_forward_for_3_step(serial_wheel):
    pathw = '3F'
    serial_wheel.write(pathw.encode("utf-8"))
    print("go forward---------------------------------")
    while (True):
        if isComplete(serial_wheel) == True:
            break

def go_back(serial_wheel):
    pathw = '1B'
    serial_wheel.write(pathw.encode("utf-8"))
    print("go back-----------------------------------")
    while (True):
        if isComplete(serial_wheel) == True:
            break
def go_back_for_change(serial_wheel):
    pathw = '1Y'
    serial_wheel.write(pathw.encode("utf-8"))
    print("go back(y)-----------------------------------")
    while (True):
        if isComplete(serial_wheel) == True:
            break

def turn_North(serial_wheel):
    pathw = '1N'
    serial_wheel.write(pathw.encode("utf-8"))
    print("turn North---------------------------------")
    while (True):
        if isComplete(serial_wheel) == True:
            break


def turn_South( serial_wheel):
    pathw = '1S'
    serial_wheel.write(pathw.encode("utf-8"))
    print("turn South--------------------------------")
    while (True):
        if isComplete(serial_wheel) == True:
            break

def turn_East( serial_wheel):
    pathw = '1E'
    serial_wheel.write(pathw.encode("utf-8"))
    print("turn East--------------------------------")
    while (True):
        if isComplete(serial_wheel) == True:
            break

def turn_West( serial_wheel):
    pathw = '1W'
    serial_wheel.write(pathw.encode("utf-8"))
    print("turn West--------------------------------")
    while (True):
        if isComplete(serial_wheel) == True:
            break


def go_forward_1(serial_wheel):  # 向前走三分之一
    pathw = '1U'
    serial_wheel.write(pathw.encode("utf-8"))
    print("向前走１／３ -------------------------------")
    while (True):
        if isComplete(serial_wheel) == True:
            break


def go_forward_2(serial_wheel):  # 向后走三分之一
    pathw = '1V'
    serial_wheel.write(pathw.encode("utf-8"))
    print("向后走１／３--------------------------------")
    while (True):
        if isComplete(serial_wheel) == True:
            break

# mark
def go_forward_3(serial_wheel):  # 向后走三分之一
    pathw = '1z'
    serial_wheel.write(pathw.encode("utf-8"))
    print("内圈调整向后走--------------------------------")
    while (True):
        if isComplete(serial_wheel) == True:
            break


def go_forward_slow(serial_wheel):
    pathw = '1X'
    serial_wheel.write(pathw.encode("utf-8"))
    print("缓慢向前--------------------------------")
    while (True):
        if isComplete(serial_wheel) == True:
            break

def go_back_slow(serial_wheel):
    pathw = '1T'
    serial_wheel.write(pathw.encode("utf-8"))
    print("缓慢向前--------------------------------")
    while (True):
        if isComplete(serial_wheel) == True:
            break

# -----------------------------------------------------------　-外圈结束

def stop(serial_wheel):
    pathw = '1M'
    serial_wheel.write(pathw.encode("utf-8"))
    print("stop now  -----------------------------------")
    while (True):
        if isComplete(serial_wheel) == True:
            break

def stop_for_in(serial_wheel):
    pathw = '1M'
    serial_wheel.write(pathw.encode("utf-8"))
    print("stop now  -----------------------------------")
    while (True):
        if isComplete(serial_wheel) == True:
            break


def start_electromagnet(serial_wheel):
    pathw = '1O'
    serial_wheel.write(pathw.encode("utf-8"))
    print("start electromagnet  ------------------------")
    while (True):
        if isComplete(serial_wheel) == True:
            break


# ----------------------------------------------------------内圈开始

def go_forward_in( serial_wheel):
    pathw = '1A'
    serial_wheel.write(pathw.encode("utf-8"))
    print("向前走　　-----------------------------------")
    while (True):
        if isComplete(serial_wheel) == True:
            break

def go_forward_in_for_2_step( serial_wheel):
    pathw = '2A'
    serial_wheel.write(pathw.encode("utf-8"))
    print("向前走　　-----------------------------------")
    while (True):
        if isComplete(serial_wheel) == True:
            break

def go_forward_in_and_check( serial_wheel):
    pathw = '1A'
    serial_wheel.write(pathw.encode("utf-8"))
    print("向前走　　-----------------------------------")
    back = isComplete_in(serial_wheel)
    return back

def back_electomagent(serial_wheel):
    pathw = '1o'
    serial_wheel.write(pathw.encode("utf-8"))
    print("back_electomagent ------------------------")
    while (True):
        if isComplete(serial_wheel) == True:
            break

def adjust_in( serial_wheel):
    pathw = '1Z'
    serial_wheel.write(pathw.encode("utf-8"))
    print("外圈转内圈-----------------------------------")
    while (True):
        if isComplete(serial_wheel) == True:
            break

def adjust_in_2( serial_wheel):
    pathw = '2Z'
    serial_wheel.write(pathw.encode("utf-8"))
    print("外圈转内圈-----------------------------------")
    while (True):
        if isComplete(serial_wheel) == True:
            break
def engine_adjust(serial_wheel):
    pathw = '1J'
    serial_wheel.write(pathw.encode("utf-8"))
    print("外圈转内圈-----------------------------------")
    while (True):
        if isComplete(serial_wheel) == True:
            break

def go_back_in(serial):
    pathw = '1C'
    serial.write(pathw.encode("utf-8"))
    print("内圈后退-----------------------------------")
    while (True):
        if isComplete(serial) == True:
            break

# ----------------------------------------------------------内圈开始
def isComplete(serial):
    s = serial.readline()
    print("waiting for feedback...", s)
    if b'K' in s:
        print("complete!--------------------------------------")
        return True

def IN_position_Go(serial):
    pathw = '1Q'
    serial.write(pathw.encode("utf-8"))
    print("内圈后退-----------------------------------")
    while (True):
        if isComplete(serial) == True:
            break
def IN_position_Go_half(serial):
    pathw = '1P'
    serial.write(pathw.encode("utf-8"))
    print("内圈后退-----------------------------------")
    while (True):
        if isComplete(serial) == True:
            break

# def isDetected(serial):
#     while(1):
#         s = serial.readline()
#         print("waiting for feedback...", s)
#         if b'Q\r\n' == s:
#             print("something is detected---------------------------")
#             return True

def isComplete_in(serial1):
    while(1):
        e = serial1.readline()
        print("waiting for wheel feisComplete_inedback....", e)
        if b'Y' == e or b'YY' == e:
            print("something is detected---------------------------")
            return 1
        elif b'K' == e or b'KK' == e or b'KKK' == e:
            print("一格到达-------------------------------------")
            return 2
        # elif b'KK' == e and box_num > 0:
        #     print("box_num: ",box_num,'\n')
        #     print("一格到达-------------------------------------")
        #     return 2
        elif b'KY' == e or b'YK' == e or b'KKY' == e or b'KKKY' == e or b'YKKY'== e or b'YKKKY'==e:
            print("一格到达-------------------------------------")
            return 3


def MPU_init(serial_wheel):
    pathw = '1I'
    serial_wheel.write(pathw.encode("utf-8"))
    print("MPU init ------------------------------")
    while (True):
        if isComplete(serial_wheel) == True:
            break



#
if __name__ == '__main__':
    print("start\n")
    time.sleep(3)
    my_serial = serial_init()
    go_forward_3(my_serial)

