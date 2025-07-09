from AbstractMessage import AbstractMessage

class FaceUvFinishMessage(AbstractMessage):
    def __init__(self, idMeshPackage):
        super().__init__('FaceUvFinishMessage')
        self.idMeshPackage = idMeshPackage
    
    # 设置array package的接口
    def setIdArrayPackage(self, idArrayPackage):
        self.idArrayPackage = idArrayPackage

    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream):
        # 发送mesh package
        print('face uv 发送完成')
        stream.writeUInt(self.idArrayPackage)
        stream.writeUInt(self.idMeshPackage)

    def receive(self, stream, messageManager):
        pass