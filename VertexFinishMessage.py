from AbstractMessage import AbstractMessage

# 节点发送完成时的消息
class VertexFinishMessage(AbstractMessage):
    def __init__(self, idPackage):
        super().__init__('VertexFinishMessage')
        # mesh包的id
        self.idPackage = idPackage
    
    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream):
        # 发送package id
        stream.writeUInt(self.idPackage)

    def receive(self, stream, messageManager):
        pass