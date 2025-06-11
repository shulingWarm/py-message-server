from AbstractMessage import AbstractMessage
from ImageReceiveMessage import ImageReceiveMessage

class ImageRowData(AbstractMessage):
    def __init__(self,imgData, imgWidth, idRow, idPackage):
        super().__init__('ImageRowData')
        pass

    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream):
        pass

    def receive(self, stream, messageManager):
        # 接收package id
        idPackage = stream.readUInt()
        # 从包管理器里面获取图片信息
        imagePackage = stream.getPackageManager().getRemotePackage(idPackage)
        # 从图片package里面获取原始的图片宽度
        image = imagePackage.image
        # 读取图片的宽度
        imgWidth = image.width
        # 读取本次传输的行id
        idRow = stream.readUInt()
        print('收到行消息: ', idRow)
        # 读取图片的当前行数据
        rowData = stream.readData(imgWidth*4)
        # 将读取到的数据写到图片里面
        image.setRowPixel(idRow, rowData)
        # 请求发送下一行的数据
        messageManager.sendMessage(ImageReceiveMessage(idPackage, idRow+1))
