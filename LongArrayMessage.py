from AbstractMessage import AbstractMessage
from LongArrayPackage import LongArrayPackage

class LongArrayMessage(AbstractMessage):
    def __init__(self, dataArray, finishFunctor):
        super().__init__('LongArrayMessage')
        self.dataArray = dataArray
        self.finishFunctor = finishFunctor

    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream):
        # 在本地建立数据包
        idPackage = stream.getPackageManager().registerPackageTask(
            LongArrayPackage(self.dataArray, self.finishFunctor)
        )
        # 发送数据包的id
        stream.writeUInt(idPackage)
        # 写入数据序列的长度
        stream.writeUInt(len(self.dataArray))

    def receive(self, stream, messageManager):
        pass
        