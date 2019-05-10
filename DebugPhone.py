import os
import re
import time

def PowerButtonEvent():
    print("按下电源键")
    os.system("adb shell input keyevent 26")
    time.sleep(3)
    
    pass

def UnlockPhone():
    PowerButtonEvent()
    time.sleep(3)
    print("滑动解锁")
    os.system("adb shell input swipe 300 1000 300 500")
    time.sleep(3)

def LoadWX():
    print("启动微信")
    os.system("adb shell am start -n com.tencent.mm/.ui.LauncherUI")
    time.sleep(3)
    pass

# 文本输入坐标：X:534 Y:1743
def MoveWXText():
    print("移动到发送文本框")
    os.system("adb shell input tap 534 1743")
    time.sleep(3)
    pass

def InputText(text):
    print("输入文本："+text)
    os.system("adb shell input text "+text)
    time.sleep(3)
    pass

# 文本发送按钮坐标：X:1018Y:949
def SendText():
    print("点击发送按钮")
    os.system("adb shell input tap 1018 949")
    time.sleep(3)
    pass

def ReadUIXML():
    os.system("adb shell uiautomator dump /data/local/tmp/uidump.xml")
    time.sleep(4)
    os.system("adb pull /data/local/tmp/uidump.xml")
    time.sleep(3)
    pass

def ReadXMLfile(path):
    xml = open(path,'r')
    return xml
    pass

def reToLocation(chatroomName,xml):
    sstr = "text=" + chatroomName + ".+" + "/>"
    result = re.match(sstr,xml)
    return result

UnlockPhone()
LoadWX()
MoveWXText()
InputText("test")
SendText()
PowerButtonEvent()