from AbstractMessage import AbstractMessage

class FinishFaceMessage(AbstractMessage):
    def __init__(self,idPackage):
        super().__init__('FinishFaceMessage')
        self.idPackage = idPackage

    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream):
        # 发送消息，表明id package 已经发送完了
        stream.writeUInt(self.idPackage)

    def receive(self, stream, messageManager):
        pass