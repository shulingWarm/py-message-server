from AbstractMessage import AbstractMessage
from MeshGenServer import MeshGenServer, MeshPostProcessInterface
from MeshMessage import MeshMessage
from NumpyMeshSolver import NumpyMeshSolver

# 回传mesh消息用到的回调
# 这是mesh完成后调用的接口
class MeshFinishCallback(MeshPostProcessInterface):
    def __init__(self, messageManager, idImagePackage):
        self.messageManager = messageManager
        # 需要记录当初原始的图片id
        self.idImagePackage = idImagePackage

    def meshProcess(self,mesh):
        # 这里需要把mesh封装成mesh solver
        meshSolver = NumpyMeshSolver(mesh.vertexList,
            mesh.faceList, mesh.vertexUvList, 
            mesh.faceUvList, mesh.textureData, mesh.textureMetallic
        )
        self.messageManager.sendMessage(MeshMessage(meshSolver, self.idImagePackage))

class HunyuanMeshGenMessage(AbstractMessage):
    def __init__(self):
        super().__init__('HunyuanMeshGenMessage')

    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream):
        pass

    def receive(self, stream, messageManager):
        # 接收目标图片id
        infoId = stream.readUInt()
        # 从包管理器里面获取图片信息
        imagePackage = stream.getPackageManager().getRemotePackage(infoId)
        image = imagePackage.image
        # 获取mesh gen server
        server = MeshGenServer.serverInstance
        # 调用server里面读取图片的过程
        server.generateMesh(image.getImageImpl(), MeshFinishCallback(messageManager, infoId))