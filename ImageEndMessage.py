from AbstractMessage import AbstractMessage
from ImageSolver import ImageSolver
from ImagePackage import ImagePackage

class ImageEndMessage(AbstractMessage):
    def __init__(self):
        super().__init__('ImageEndMessage')

    # 需要根据数据流来发送
    def send(self, stream):
        pass

    def receive(self, stream, messageManager):
        # 读取long array package
        arrayPackageId = stream.readUInt()
        # 读取图片的宽高
        imgWidth = stream.readUInt()
        imgHeight = stream.readUInt()
        # 读取用于存储图片package的id
        imgPackageId = stream.readUInt()
        # 打开long array的package
        arrayPackage = stream.getPackageManager().getRemotePackage(arrayPackageId)
        # 从long array package里面取出bytearray
        imgDataArray = arrayPackage.dataArray
        # 用array里面的信息构建image
        tempImage = ImageSolver(imgWidth,imgHeight,imgDataArray)
        # 用Image构造ImagePackage
        imagePackage = ImagePackage(tempImage)
        # 记录图片的package
        stream.getPackageManager().registerRemotePackage(imgPackageId, imagePackage)