import os
import re
import time
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import itchat
from itchat.content import *

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
    temp = numtozh(int(temp))
    weather = soup.find('div', attrs={'class': 'wea_weather clearfix'}).b.getText()
    sd = soup.find('div', attrs={'class': 'wea_about clearfix'}).span.getText()
    sd_num = re.search(r'\d+', sd).group()
    sd_num_zh = numtozh(int(sd_num))
    sd = sd.replace(sd_num, sd_num_zh)
    wind = soup.find('div', attrs={'class': 'wea_about clearfix'}).em.getText()
    aqi = soup.find('div', attrs={'class': 'wea_alert clearfix'}).em.getText()
    aqi_num = re.search(r'\d+', aqi).group()
    aqi_num_zh = numtozh(int(aqi_num))
    aqi = aqi.replace(aqi_num, aqi_num_zh).replace(' ', ',空气质量')
    info = soup.find('div', attrs={'class': 'wea_tips clearfix'}).em.getText()
    sd = sd.replace(' ', '百分之').replace('%', '')
    aqi = 'aqi' + aqi
    info = info.replace('，', ',')
    # 获取今天的日期
    #today = datetime.now().date().strftime('%Y年%m月%d日')
    # 将获取的信息拼接成一句话
    BJtext = '早上好！北京今天天气%s\n温度%s摄氏度\n%s\n%s\n%s\n%s' % \
           ( weather, temp, sd, wind, aqi, info)

    # 下载墨迹天气主页源码
    res = requests.get('https://tianqi.moji.com/weather/china/hubei/wuhan', headers=headers)
    # 用BeautifulSoup获取所需信息
    soup = BeautifulSoup(res.text, "html.parser")
    temp = soup.find('div', attrs={'class': 'wea_weather clearfix'}).em.getText()
    temp = numtozh(int(temp))
    weather = soup.find('div', attrs={'class': 'wea_weather clearfix'}).b.getText()
    sd = soup.find('div', attrs={'class': 'wea_about clearfix'}).span.getText()
    sd_num = re.search(r'\d+', sd).group()
    sd_num_zh = numtozh(int(sd_num))
    sd = sd.replace(sd_num, sd_num_zh)
    wind = soup.find('div', attrs={'class': 'wea_about clearfix'}).em.getText()
    aqi = soup.find('div', attrs={'class': 'wea_alert clearfix'}).em.getText()
    aqi_num = re.search(r'\d+', aqi).group()
    aqi_num_zh = numtozh(int(aqi_num))
    aqi = aqi.replace(aqi_num, aqi_num_zh).replace(' ', ',空气质量')
    info = soup.find('div', attrs={'class': 'wea_tips clearfix'}).em.getText()
    sd = sd.replace(' ', '百分之').replace('%', '')
    aqi = 'aqi' + aqi
    info = info.replace('，', ',')

    WHtext = '武汉今天天气%s\n温度%s摄氏度\n%s\n%s\n%s\n%s' % \
           (weather, temp, sd, wind, aqi, info)

    text = BJtext + "\n\n" + WHtext
    return text



def get_news(url):
    # res = requests.get('https://mp.weixin.qq.com/s/P6e8iZLx7fu-ptYDchjxPw', headers=headers)
    res = requests.get(url, headers=headers)

    # 用BeautifulSoup获取所需信息
    soup = BeautifulSoup(res.text, "html.parser")
    info = soup.find_all("span",attrs={"style":"color: rgb(19, 36, 32); font-size: 18px;"})
    Info6 = str(info[6])
    pattern = "6、.+；"
    Info6 = re.findall(pattern,Info6)[0]
    News = []
    for i in range(len(info)):
        News.append(info[i].string)
    News[6] = Info6

    for i in News:
        print(i)
    return News

# 自动获取每日新闻公众号
@itchat.msg_register(TEXT, isMpChat=True)
def send_GZH_dayly_news(msg):
    try:
        ID = msg['User']['NickName']
        Content = msg['Content']
        
        # if ID == "今日快速报":
        if True:
            # 获取天气
            weather_info = get_weather()

            # 获取新闻
            News_info = get_news("https://mp.weixin.qq.com/s/P6e8iZLx7fu-ptYDchjxPw")

            # 发送到群里
            groupName = itchat.search_chatrooms(name = "测试")[0]
            groupName.send(weather_info)

        print(msg)
    except:
        pass
    pass

# ======================================================================
# ======================================================================

# 获取当天天气情况


# 


# 登录微信
itchat.auto_login()

# # 获取群聊名字
groupList = itchat.get_chatrooms(update = True)
groupName = itchat.search_chatrooms(name = "测试")
for i in groupList:
    print(i['NickName'])
itchat.run()