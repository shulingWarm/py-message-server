from AbstractMessage import AbstractMessage

class MessageManager:
    def __init__(self, stream):
        # 记录stream信息
        self.stream = stream
        # message tag的基础offset
        self.tagOffset = 20000
        # 消息头字典
        self.messageTagMap = {}
        # 所有的message列表
        self.messageList = []

    # 判断某个消息tag是否可能是一个被管理的tag
    def isTagInRange(self, tag):
        return tag >= self.tagOffset

    # 注册消息
    def registerMessage(self, message:AbstractMessage):
        # 需要确保名字不是空的
        if len(message.name) == 0:
            raise ValueError("Empty message name.")
        elif message.name in self.messageTagMap:
            raise ValueError(f"Repeat message name: {message.name}")
        # 注册新的message项
        self.messageTagMap[message.name] = len(self.messageList)
        self.messageList.append(message)

    # 发送消息
    def sendMessage(self, message:AbstractMessage):
        # 确认消息名是否在字典内
        if message.name not in self.messageTagMap:
            raise ValueError(f"Unknown message: {message.name}")
        # 获取消息头
        messageHeader = self.messageTagMap[message.name] + self.tagOffset
        # 通过stream发送消息头
        self.stream.writeUInt(messageHeader)
        # 调用消息内部的发送逻辑
        message.send(self.stream)

    # 接收消息
    def receiveMessage(self, tag:int):
        # 判断tag是否在范围内
        if tag >= self.tagOffset:
            # 判断实际的长度是否合法
            tag = tag - self.tagOffset
            if tag >= 0 and tag < len(self.messageList):
                # 调用消息的接收逻辑
                self.messageList[tag].receive(self.stream, self)
            else:
                raise ValueError(f"Unknon tag: {tag}")