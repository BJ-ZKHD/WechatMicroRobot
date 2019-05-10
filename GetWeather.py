import os
import re
import time
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import os
import re
import time
import schedule

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit'
                      '/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safar'
                      'i/537.36',
    }

def numtozh(num):
    num_dict = {1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七',
                8: '八', 9: '九', 0: '零'}
    num = int(num)
    if 100 <= num < 1000:
        b_num = num // 100
        s_num = (num-b_num*100) // 10
        g_num = (num-b_num*100) % 10
        if g_num == 0 and s_num == 0:
            num = '%s百' % (num_dict[b_num])
        elif s_num == 0:
            num = '%s百%s%s' % (num_dict[b_num], num_dict.get(s_num, ''), num_dict.get(g_num, ''))
        elif g_num == 0:
            num = '%s百%s十' % (num_dict[b_num], num_dict.get(s_num, ''))
        else:
            num = '%s百%s十%s' % (num_dict[b_num], num_dict.get(s_num, ''), num_dict.get(g_num, ''))
    elif 10 <= num < 100:
        s_num = num // 10
        g_num = (num-s_num*10) % 10
        if g_num == 0:
            g_num = ''
        num = '%s十%s' % (num_dict[s_num], num_dict.get(g_num, ''))
    elif 0 <= num < 10:
        g_num = num
        num = '%s' % (num_dict[g_num])
    elif -10 < num < 0:
        g_num = -num
        num = '零下%s' % (num_dict[g_num])
    elif -100 < num <= -10:
        num = -num
        s_num = num // 10
        g_num = (num-s_num*10) % 10
        if g_num == 0:
            g_num = ''
        num = '零下%s十%s' % (num_dict[s_num], num_dict.get(g_num, ''))
    return num

def get_weather():
    # 下载墨迹天气主页源码
    res = requests.get('http://tianqi.moji.com/', headers=headers)
    # 用BeautifulSoup获取所需信息
    soup = BeautifulSoup(res.text, "html.parser")
    temp = soup.find('div', attrs={'class': 'wea_weather clearfix'}).em.getText()
    temp = temp
    weather = soup.find('div', attrs={'class': 'wea_weather clearfix'}).b.getText()
    sd = soup.find('div', attrs={'class': 'wea_about clearfix'}).span.getText()
    sd_num = re.search(r'\d+', sd).group()
    sd_num_zh = sd_num
    sd = sd.replace(sd_num, sd_num_zh)
    wind = soup.find('div', attrs={'class': 'wea_about clearfix'}).em.getText()
    aqi = soup.find('div', attrs={'class': 'wea_alert clearfix'}).em.getText()
    aqi_num = re.search(r'\d+', aqi).group()
    aqi_num_zh = aqi_num
    aqi = aqi.replace(aqi_num, aqi_num_zh).replace(' ', ',空气质量')
    info = soup.find('div', attrs={'class': 'wea_tips clearfix'}).em.getText()
    sd = sd.replace(' ', '百分之').replace('%', '')
    aqi = '空气指数' + aqi
    info = info.replace('，', ',')
    # 获取今天的日期
    #today = datetime.now().date().strftime('%Y年%m月%d日')
    # 将获取的信息拼接成一句话
    BJtext = '早上好！北京今天天气%s\n温度%s摄氏度\n%s\n%s\n%s\n%s' % \
           ( weather, temp, sd, wind, aqi, info)
    BJtextList = []

    BJtextList.append("早上好！北京今天天气" + weather)
    BJtextList.append("温度" + temp + "摄氏度")
    BJtextList.append(sd)
    BJtextList.append(wind)
    BJtextList.append(aqi)
    BJtextList.append(info)

    # 下载墨迹天气主页源码
    res = requests.get('https://tianqi.moji.com/weather/china/hubei/wuhan', headers=headers)
    # 用BeautifulSoup获取所需信息
    soup = BeautifulSoup(res.text, "html.parser")
    temp = soup.find('div', attrs={'class': 'wea_weather clearfix'}).em.getText()
    temp = temp
    weather = soup.find('div', attrs={'class': 'wea_weather clearfix'}).b.getText()
    sd = soup.find('div', attrs={'class': 'wea_about clearfix'}).span.getText()
    sd_num = re.search(r'\d+', sd).group()
    sd_num_zh = sd_num
    sd = sd.replace(sd_num, sd_num_zh)
    wind = soup.find('div', attrs={'class': 'wea_about clearfix'}).em.getText()
    aqi = soup.find('div', attrs={'class': 'wea_alert clearfix'}).em.getText()
    aqi_num = re.search(r'\d+', aqi).group()
    aqi_num_zh = aqi_num
    aqi = aqi.replace(aqi_num, aqi_num_zh).replace(' ', ',空气质量')
    info = soup.find('div', attrs={'class': 'wea_tips clearfix'}).em.getText()
    sd = sd.replace(' ', '百分之').replace('%', '')
    aqi = '空气指数' + aqi
    info = info.replace('，', ',')

    WHtext = '武汉今天天气%s\n温度%s摄氏度\n%s\n%s\n%s\n%s' % \
           (weather, temp, sd, wind, aqi, info)

    text = BJtext + "\n\n" + WHtext

    BJtextList.append("\n\n")
    BJtextList.append("早上好！武汉今天天气" + weather)
    BJtextList.append("温度" + temp + "摄氏度")
    BJtextList.append(sd)
    BJtextList.append(wind)
    BJtextList.append(aqi)
    BJtextList.append(info)
    return BJtextList

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

def InputChineseText(text):
    print("输入中文文本")
    if type(text) == str:
        os.system("adb shell input text "+text)
        time.sleep(3)
    elif type(text) == list:
        for i in text:
            os.system("adb shell am broadcast -a ADB_INPUT_TEXT --es msg " + i+"\n")
            os.system("adb shell input keyevent 66")
            time.sleep(3)

# 文本发送按钮坐标：X:1017Y:1746
def SendText():
    print("点击发送按钮")
    os.system("adb shell input tap 1018 1746")
    time.sleep(1)
    os.system("adb shell input tap 1018 1695")
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

def PhoneSendWeather():
    weather_info = get_weather()
    UnlockPhone()
    LoadWX()
    MoveWXText()
    InputChineseText(weather_info)
    SendText()
    PowerButtonEvent()

# schedule.every().day.at("1:09").do(PhoneSendWeather)
# schedule.every().day.at("08:15").do(PhoneSendWeather)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
#     print("等待执行天气任务")
PhoneSendWeather()