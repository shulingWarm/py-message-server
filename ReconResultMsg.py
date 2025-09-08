from AbstractMessage import AbstractMessage

class ReconResultMsg(AbstractMessage):
    def __init__(self,idPackage,requestIdPackage):
        super().__init__('ReconResultMsg')
        # 记录对应的long array package id
        self.idPackage = idPackage
        # 记录这个重建结果属于当时的哪个package
        self.requestIdPackage = requestIdPackage

    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream):
        # 发送package id
        stream.writeUInt(self.idPackage)
        # 删除这个本地package
        stream.getPackageManager().deletePackageInfo(self.idPackage)
        # 发送当初所属的请求包的id
        stream.writeUInt(self.requestIdPackage)

    def receive(self, stream, messageManager):
        pass