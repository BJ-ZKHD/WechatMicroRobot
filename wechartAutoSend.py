import itchat
from itchat.content import *

# 监听是谁给我发消息
# @itchat.msg_register(INCOME_MSG)
# def text_reply(msg):
#     itchat.send("您发送了：\'%s\'\n微信目前处于python托管，你的消息我会转发到手机，谢谢" %
#                 (msg['Text']), toUserName=msg['FromUserName'])
# 自动复读
# @itchat.msg_register(TEXT, isFriendChat=True, isGroupChat=True, isMpChat=True)
# def simple_reply(msg):
#     return 'I received: %s' % msg.text

# 自动获取每日新闻公众号
@itchat.msg_register(TEXT, isMpChat=True)
def send_GZH_dayly_news(msg):
    try:
        ID = msg['User']['NickName']
        Content = msg['Content']
        

        if ID == "今日快速报":
            groupName = itchat.search_chatrooms(name = "K78")[0]
            groupName.send(Content)

        print(msg)
    except:
        pass
    pass

itchat.auto_login(hotReload=True)
groupList = itchat.get_chatrooms(update=True)
groupName = itchat.search_chatrooms(name = "测试")
for i in groupList:
    print(i['NickName'])
itchat.run()



