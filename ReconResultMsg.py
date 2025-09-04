from AbstractMessage import AbstractMessage

class ReconResultMsg(AbstractMessage):
    def __init__(self,idPackage):
        super().__init__('ReconResultMsg')
        # 记录对应的long array package id
        self.idPackage = idPackage

    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream):
        # 发送package id
        stream.writeUInt(self.idPackage)
        # 删除这个本地package
        stream.getPackageManager().deletePackageInfo(self.idPackage)

    def receive(self, stream, messageManager):
        pass