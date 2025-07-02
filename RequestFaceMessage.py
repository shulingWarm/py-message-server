from AbstractMessage import AbstractMessage
from FaceArrayBack import FaceArrayBack
from FinishFaceMessage import FinishFaceMessage

class RequestFaceMessage(AbstractMessage):
    def __init__(self):
        super().__init__('RequestFaceMessage')

    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream):
        pass

    def receive(self, stream, messageManager):
        # 读取package id
        idPackage = stream.readUInt()
        # 读取请求的face id
        idFace = stream.readUInt()
        # 获取mesh
        meshPackage = stream.getPackageManager().getLocalPackage(idPackage)
        mesh = meshPackage.mesh
        # 检查是否已经发送完了
        if idFace >= mesh.getMeshFaceNum():
            print('Face Finish')
            messageManager.sendMessage(FinishFaceMessage(idPackage))
        else:
            print('Face: ', idFace)
            # 获取face序列
            faceList = mesh.getFaceArray(idFace, meshPackage.vertexSendNum)
            # 把face序列发出去
            messageManager.sendMessage(FaceArrayBack(idPackage, idFace, faceList))
