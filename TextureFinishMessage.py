from AbstractMessage import AbstractMessage
from ArrayFinishMessage import ArrayFinishMessage

class TextureFinishMessage(ArrayFinishMessage):
    def __init__(self, idMeshPackage, textureChannelNum=3):
        super().__init__('TextureFinishMessage')
        self.idMeshPackage = idMeshPackage
        self.textureChannelNum = textureChannelNum
    
    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream):
        print('texture 发送完成')
        # 发送mesh package
        stream.writeUInt(self.idMeshPackage)
        stream.writeUInt(self.idArrayPackage)
        # 发送mesh的channel数量
        stream.writeUInt(self.textureChannelNum)

    def receive(self, stream, messageManager):
        pass