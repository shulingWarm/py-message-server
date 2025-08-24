from AbstractMessage import AbstractMessage
from LongArrayBackMessage import LongArrayBackMessage

class RequestLongArrayMessage(AbstractMessage):
    def __init__(self, idPackage=0, idData=0):
        super().__init__('RequestLongArrayMessage')
        self.idPackage=idPackage
        self.idData = idData

    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream):
        # 写入请求的包id
        stream.writeUInt(self.idPackage)
        # 写入请求的数据id
        stream.writeUInt(self.idData)

    def receive(self, stream, messageManager):
        # 接收package id
        idPackage = stream.readUInt()
        # 读取请求的id
        idData = stream.readUInt()
        # 获取package
        dataPackage = stream.getPackageManager().getLocalPackage(idPackage)
        # 判断数据是不是已经超了
        if(idData >= dataPackage.getDataLength()):
            print('长数组发送完成')
            # 执行array发送完的后续逻辑
            dataPackage.finishFunctor(messageManager, idPackage)
        else:
            print('发送数据片段', idData, '/', dataPackage.getDataLength())
            # 从package里面获取片段
            dataSlice = dataPackage.getDataArraySlice(idData, dataPackage.byteNumPerSend)
            # 发送long array的回传消息
            messageManager.sendMessage(LongArrayBackMessage(idPackage, 
                idData, dataSlice))

# 这是一个静态函数，用于生成新的请求
def staticLongArrayRequest(messageManager, idPackage, idData):
    # 新建一个request的message
    requestMessage = RequestLongArrayMessage(idPackage, idData)
    # 把消息发送出去
    messageManager.sendMessage(requestMessage)