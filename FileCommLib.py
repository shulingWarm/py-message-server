import FileLib
from LongArrayMessage import LongArrayMessage

# 文件通信相关的逻辑

# 发送文件
# 同时需要传入发送完成时的回调
def sendFile(filePath, messageManager, finishFunctor):
    # 将二进制文件读取到bytearray
    fileByteArray = FileLib.read_file_to_bytearray(filePath)
    if(fileByteArray is None):
        raise RuntimeError('fileByteArray is None')
    longArrayMessage = LongArrayMessage(fileByteArray, finishFunctor)
    # 把消息发出去
    messageManager.sendMessage(longArrayMessage)