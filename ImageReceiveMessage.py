from AbstractMessage import AbstractMessage

# 这是当收到图片消息时的回传
class ImageReceiveMessage(AbstractMessage):
    def __init__(self, infoId, idRow):
        super().__init__('ImageReceiveMessage')
        self.infoId = infoId
        # idRow 表示请求发送的下一个图片行
        self.idRow = idRow

    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream):
        # 写入info id
        stream.writeUInt(self.infoId)
        # 写入期望下一行发送的行
        stream.writeUInt(self.idRow)


    # python端暂时不实现这里的接收逻辑，如果后面要需要再说
    def receive(self, stream, messageManager):
        pass