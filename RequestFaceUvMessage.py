from AbstractMessage import AbstractMessage
from LongArrayMessage import LongArrayMessage
from FaceUvFinishMessage import FaceUvFinishMessage
from ArrayFinishMessageFunctor import ArrayFinishMessageFunctor

class RequestFaceUvMessage(AbstractMessage):
    def __init__(self):
        super().__init__('RequestFaceUvMessage')

    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream):
        pass

    def receive(self, stream, messageManager):
        # 读取mesh package
        idMeshPackage = stream.readUInt()
        # 发送完成后的后处理消息
        finishMessage = FaceUvFinishMessage(idMeshPackage)
        # 构造long array传输完成时的functor
        finishFunctor = ArrayFinishMessageFunctor(finishMessage)
        # 获取mesh 
        meshPackage = stream.getPackageManager().getLocalPackage(idMeshPackage)
        mesh = meshPackage.mesh
        # 从mesh里面获取face uv
        faceUvData = mesh.getFaceUvByteArray()
        # 发送long array message
        messageManager.sendMessage(LongArrayMessage(faceUvData,finishFunctor))