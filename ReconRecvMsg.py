from AbstractMessage import AbstractMessage

# 收到重建请求后，发送已经收到重建消息
# 这是为了通知对方开始传送重建需要的图片
class ReconRecvMsg(AbstractMessage):
    def __init__(self, idPackage):
        super().__init__('ReconRecvMsg')
        # 记录接收到的是哪个消息包
        self.idPackage = idPackage

    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream):
        # 发送package
        stream.writeUInt(self.idPackage)

    def receive(self, stream, messageManager):
        pass