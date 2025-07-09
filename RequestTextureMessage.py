from AbstractMessage import AbstractMessage
from TextureFinishMessage import TextureFinishMessage
from ArrayFinishMessageFunctor import ArrayFinishMessageFunctor
from LongArrayMessage import LongArrayMessage

class RequestTextureMessage(AbstractMessage):
    def __init__(self):
        super().__init__('RequestTextureMessage')

    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream):
        pass

    def receive(self, stream, messageManager):
        # 读取id mesh package
        idMeshPackage = stream.readUInt()
        # 获取mesh
        meshPackage = stream.getPackageManager().getLocalPackage(idMeshPackage)
        mesh = meshPackage.mesh
        # 从mesh里面获取texture的channel大小
        width, height, channel = mesh.getTextureSize()
        # 获取texture数据
        textureData = mesh.getTextureByteArray()
        # 准备发送texture完成的消息
        finishMessage = TextureFinishMessage(idMeshPackage, channel)
        # 封装成functor
        finishFunctor = ArrayFinishMessageFunctor(finishMessage)
        # 发送long array的消息
        messageManager.sendMessage(LongArrayMessage(textureData, finishFunctor))