from AbstractMessage import AbstractMessage
from ImageSolver import ImageSolver
from ImagePackage import ImagePackage
from ImageReceiveMessage import ImageReceiveMessage

class ImageMessage(AbstractMessage):
    def __init__(self, image:ImageSolver):
        super().__init__('ImageMessage')
        # 记录自身保有的图片
        self.image = image

    # 发送逻辑
    # 需要根据数据流来发送
    # python这边暂时不实现发送端
    def send(self, stream):
        pass

    def receive(self, stream, messageManager):
        # 读取package的id
        idPackage = stream.readUInt()
        # 读取图片的宽
        imgWidth = stream.readUInt()
        imgHeight = stream.readUInt()
        # 初始化一个图片
        tempImage = ImageSolver(imgWidth, imgHeight)
        # 将图片信息保存到分包管理器中
        imagePackage = ImagePackage(tempImage)
        # 将图片信息注册为远端信息
        packageManager = stream.getPackageManager()
        packageManager.registerRemotePackage(idPackage, imagePackage)
        # 回传信息，告知已经收到了数据头
        messageManager.sendMessage(ImageReceiveMessage(idPackage, 0))
        pass

    