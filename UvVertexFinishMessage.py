from AbstractMessage import AbstractMessage

class UvVertexFinishMessage(AbstractMessage):
    def __init__(self, idMeshPackage):
        super().__init__('UvVertexFinishMessage')
        self.idMeshPackage = idMeshPackage

    def setIdArrayPackage(self, idArrayPackage):
        self.idArrayPackage = idArrayPackage

    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream):
        print('完成uv vertex')
        stream.writeUInt(self.idMeshPackage)
        stream.writeUInt(self.idArrayPackage)

    def receive(self, stream, messageManager):
        pass