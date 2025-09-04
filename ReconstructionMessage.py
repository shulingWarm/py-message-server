from ReconstructionPackage import ReconstructionPackage
from AbstractMessage import AbstractMessage
from ReconRecvMsg import ReconRecvMsg


class ReconstructionMessage(AbstractMessage):
    def __init__(self):
        super().__init__('ReconstructionMessage')

    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream):
        pass

    def receive(self, stream, messageManager):
        # 接收package
        idPackage = stream.readUInt()
        # 图片的个数
        imageNum = stream.readUInt()
        packageManager = stream.getPackageManager()
        # 新建一个远端的package
        reconPackage = ReconstructionPackage(imageNum)
        # 注册远端package
        packageManager.registerRemotePackage(idPackage, reconPackage)
        # 回传收到重建消息的信息
        messageManager.sendMessage(ReconRecvMsg(idPackage))