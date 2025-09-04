from AbstractMessage import AbstractMessage

class ReconSingleImgMsg(AbstractMessage):
    def __init__(self):
        super().__init__('ReconSingleImgMsg')

    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream):
        pass

    def receive(self, stream, messageManager):
        # 读取重建包id
        reconPkgId = stream.readUInt()
        # 读取加载好的图片的id
        imgId = stream.readUInt()
        # 读取重建任务包
        reconPkg = stream.getPackageManager().getRemotePackage(reconPkgId)
        # 读取图片包
        imgPkg = stream.getPackageManager().getRemotePackage(reconPkgId)
        # 在reconPkg里面注册新的用于重建的图片
        reconPkg.rgstReconImg(imgPkg.image)