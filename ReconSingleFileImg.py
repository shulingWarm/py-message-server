from AbstractMessage import AbstractMessage
from StreamInterface import StreamInterface
from MessageManager import MessageManager
from LongArrayPackage import LongArrayPackage
from ReconstructionPackage import ReconstructionPackage

# 文件形式的message
class ReconSingleFileImg(AbstractMessage):
    def __init__(self):
        super().__init__('ReconSingleFileImg')

    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream:StreamInterface):
        pass

    def receive(self, stream:StreamInterface, messageManager:MessageManager):
        # 读取long array的package
        idArrayPackage = stream.readUInt()
        # 读取图片的格式
        imgFmt = stream.readUInt()
        # 读取重建数据包
        idReconPkg = stream.readUInt()
        # 读取里面的byte array
        tempPackage:LongArrayPackage = stream.getPackageManager().getRemotePackage(idArrayPackage)
        # 将bytearray保存成文件
        targetData = tempPackage.dataArray
        # 准备用于重建的package
        reconPkg:ReconstructionPackage = stream.getPackageManager().getRemotePackage(idReconPkg)
        # 通过文件保存数据
        reconPkg.rgstReconImgByFile(targetData, imgFmt=imgFmt)