from AbstractMessage import AbstractMessage
from MeshGenServer import MeshGenServer, MeshPostProcessInterface
from MeshMessage import MeshMessage
from NumpyMeshSolver import NumpyMeshSolver
from TextureLibrary import saveTextureAsImage

# 回传mesh消息用到的回调
# 这是mesh完成后调用的接口
class MeshFinishCallback(MeshPostProcessInterface):
    def __init__(self, messageManager, idImagePackage, idTaskPackage):
        self.messageManager = messageManager
        # 需要记录当初原始的图片id
        self.idImagePackage = idImagePackage
        self.idTaskPackage = idTaskPackage

    def meshProcess(self,mesh):
        # 这里需要把mesh封装成mesh solver
        meshSolver = NumpyMeshSolver(mesh.vertexList,
            mesh.faceList, mesh.vertexUvList, 
            mesh.faceUvList, mesh.textureData, mesh.textureMetallic
        )
        # 把texture保存到本地
        # saveTextureAsImage(meshSolver._textureData, '/mnt/data/temp/test_texture.jpg')
        self.messageManager.sendMessage(
            MeshMessage(meshSolver, self.idImagePackage, idTaskPackage=self.idTaskPackage))

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
        # 接收远端的task message 这不需要在本地注册，只是用来方便远端知道这是来自哪一次请求的应答
        remoteTaskId = stream.readUInt()
        # 从包管理器里面获取图片信息
        imagePackage = stream.getPackageManager().getRemotePackage(infoId)
        image = imagePackage.image
        # 获取mesh gen server
        server = MeshGenServer.serverInstance
        # 调用server里面读取图片的过程
        server.generateMesh(image.getImageImpl(), 
            MeshFinishCallback(messageManager, infoId, idTaskPackage=remoteTaskId))