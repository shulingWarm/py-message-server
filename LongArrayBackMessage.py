from AbstractMessage import AbstractMessage

class LongArrayBackMessage(AbstractMessage):
    def __init__(self, idPackage, idData, dataArray):
        super().__init__('LongArrayBackMessage')
        self.idPackage = idPackage
        self.idData = idData
        self.dataArray = dataArray

    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream):
        # 发送package id
        stream.writeUInt(self.idPackage)
        # 发送数据的id
        stream.writeUInt(self.idData)
        # 发送数据的长度
        stream.writeUInt(len(self.dataArray))
        # 发送数据内容
        stream.writeData(self.dataArray)

    def receive(self, stream, messageManager):
        pass