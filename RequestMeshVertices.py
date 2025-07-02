from AbstractMessage import AbstractMessage
from VertexArrayBack import VertexArrayBack
from VertexFinishMessage import VertexFinishMessage

class RequestMeshVertices(AbstractMessage):
    def __init__(self):
        super().__init__('RequestMeshVertices')

    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream):
        pass

    def receive(self, stream, messageManager):
        # 读取id package
        idPackage = stream.readUInt()
        # 读取请求的id
        idVertex = stream.readUInt()
        # 获取idpackage
        meshPackage = stream.getPackageManager().getLocalPackage(idPackage)
        # 检查mesh是否已经发送完了所有的vertex
        if meshPackage.mesh.getVertexNum() <= idVertex:
            # 发送所有节点发送完成的消息
            print('Vertex发送完成')
            messageManager.sendMessage(VertexFinishMessage(idPackage))
        else:
            # 获取mesh里面的点列表
            vertexList = meshPackage.mesh.getVertexArray(idVertex, meshPackage.vertexSendNum)
            # 新建vertex列表回传的message
            messageManager.sendMessage(VertexArrayBack(vertexList, idPackage, idVertex))