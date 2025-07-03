

# 在python里面, package没有共同的父类
class MeshPackage:
    def __init__(self, idImagePackage, mesh):
        # 这个mesh所属的原始图片的名字
        self.idImagePackage = idImagePackage
        self.mesh = mesh
        # 节点是否已经发送完
        self.sendVerticeOk = False
        # 每次vertex发送的个数
        self.vertexSendNum = 256