

class MeshSolver:
    def __init__(self):
        pass

    # 获取总的节点个数
    def getVertexNum(self):
        pass

    # 获取mesh，从里面提取一段指定的vertex id
    def getVertexArray(self, vertexId, vertexNum):
        pass

    def getMeshFaceNum(self) -> int:
        pass

    def getFaceArray(self, faceId: int, faceNum: int) -> list:
        pass

    # 获取texture的一段指定数据
    # 这里的pixelId指的是将图片展平后的id
    # pixelId = row_id*width + col_id
    # pixelNum指的是从pixelId开始，连续获取多少个像素
    # 返回的list的格式是 [r0,g0,b0,r1,g1,b1,r2,g2,b2,...]
    def getTextureData(self, pixelId, pixelNum) -> list:
        pass

    # 获取纹理的metallic的一段指定数据
    # 获取数据的方式与getTextureData相同
    def getMetallicData(self,pixelId,pixelNum) -> list:
        pass

    # 获取texture的大小
    def getTextureSize(self) -> int:
        pass