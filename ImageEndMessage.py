from AbstractMessage import AbstractMessage

class ImageEndMessage(AbstractMessage):
    def __init__(self):
        super().__init__('ImageEndMessage')

    # 需要根据数据流来发送
    def send(self, stream):
        pass

    def receive(self, stream, messageManager):
        # 获取包id
        idPackage = stream.readUInt()
        # 获取图片数据包
        imagePackage = stream.getPackageManager().getRemotePackage(idPackage)
        # 把收到的图片保存在本地
        imagePackage.image.save('test.png')
        # 删除图片消息
        stream.getPackageManager().deleteRemotePackage(idPackage)