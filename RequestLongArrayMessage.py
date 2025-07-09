from AbstractMessage import AbstractMessage
from LongArrayBackMessage import LongArrayBackMessage

class RequestLongArrayMessage(AbstractMessage):
    def __init__(self):
        super().__init__('RequestLongArrayMessage')

    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream):
        pass

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
