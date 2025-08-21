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
        # 接收package id
        idPackage = stream.readUInt()
        # 接收起始id
        idData = stream.readUInt()
        # 接收数据长度
        dataLength = stream.readUInt()
        # 读取数据
        tempData = stream.readData(dataLength)
        # 获取package
        package = stream.getPackageManager().getRemotePackage(idPackage)
        # 向package里面写入数据
        package.recordByteArray(tempData, idData)
        # 请求下一组数据
        requestMessage = RequestLongArrayMessage(idPackage=idPackage,
            idData=idData+dataLength)
        messageManager.sendMessage(requestMessage)