from AbstractMessage import AbstractMessage

class FaceArrayBack(AbstractMessage):
    def __init__(self, idPackage, idFace, faceList):
        super().__init__('FaceArrayBack')
        self.idPackage = idPackage
        self.idFace = idFace
        self.faceList = faceList

    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream):
        # 写入包名
        stream.writeUInt(self.idPackage)
        stream.writeUInt(self.idFace)
        # 计算face的个数
        faceNum = len(self.faceList)
        if(faceNum % 3 != 0):
            raise RuntimeError('Invalid face num')
        faceNum = int(faceNum/3)
        # 发送face的个数
        stream.writeUInt(faceNum)
        # 写入face list
        stream.writeArray('int', self.faceList)
        

    def receive(self, stream, messageManager):
        pass