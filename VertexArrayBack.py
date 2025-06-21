from AbstractMessage import AbstractMessage

class VertexArrayBack(AbstractMessage):
    def __init__(self, vertexList, packageId, vertexBeginId):
        super().__init__('VertexArrayBack')
        self.vertexList = vertexList
        self.packageId = packageId
        # 记录mesh节点的起始id
        self.vertexBeginId = vertexBeginId

    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream):
        print('发送节点', self.vertexBeginId)
        vertexLength = len(self.vertexList)
        # 确认vertex list是不是3倍
        if(len(self.vertexList) % 3 != 0):
            raise RuntimeError('Vertex list not times of 3.')
        # 写入package id
        stream.writeUInt(self.packageId)
        # 发送vertex的起始id
        stream.writeUInt(self.vertexBeginId)
        # 发送列表的节点个数
        stream.writeUInt(int(vertexLength/3))
        # 从stream里面发送vertex list
        stream.writeArray('float', self.vertexList)

    def receive(self, stream, messageManager):
        pass