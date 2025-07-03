from AbstractMessage import AbstractMessage
from MeshPackage import MeshPackage

# 用于发送mesh的消息
class MeshMessage(AbstractMessage):
    def __init__(self, mesh, idImagePackage):
        super().__init__('MeshMessage')
        # 记录要发送的mesh
        self.mesh = mesh
        self.idImagePackage = idImagePackage

    def send(self, stream):
        # 新建数据头
        meshPackage = MeshPackage(self.idImagePackage, self.mesh)
        # 在本地注册数据包
        idPackage = stream.getPackageManager().registerPackageTask(MeshPackage(
            self.idImagePackage, self.mesh
        ))
        vertexNum = self.mesh.getVertexNum()
        faceNum = self.mesh.getMeshFaceNum()
        print('发送mesh, 节点个数:', vertexNum, "面个数: ", faceNum)
        # 发送数据包的id
        stream.writeUInt(idPackage)
        # 写入原始的图片id
        stream.writeUInt(self.idImagePackage)
        # 写入节点的个数
        stream.writeUInt(vertexNum)
        # 发送face的个数
        stream.writeUInt(faceNum)
        
        

    def receive(self, stream, messageManager):
        pass