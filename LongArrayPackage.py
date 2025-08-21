

# 获取bytearray片段的函数
def getDataArraySlice(dataArray, idByte, byteNum):
    """
    从bytearray中提取指定起始位置和长度的片段
    
    参数:
    dataArray: bytearray - 原始字节数组
    idByte: int - 起始字节索引（0为起始位置）
    byteNum: int - 需要提取的字节数
    
    返回:
    bytearray - 提取到的字节片段（当参数无效时返回空bytearray）
    """
    # 检查参数有效性
    if not isinstance(dataArray, bytearray) or byteNum < 0:
        return bytearray()
    
    length = len(dataArray)
    
    # 处理idByte为负数的索引转换
    if idByte < 0:
        idByte = max(0, length + idByte)
    
    # 当起始索引超出有效范围时返回空bytearray
    if idByte >= length or idByte < 0:
        return bytearray()
    
    # 计算实际可提取的字节数
    end = min(idByte + byteNum, length)
    return dataArray[idByte:end]

class LongArrayPackage:
    def __init__(self,dataArray,finishFunctor):
        self.dataArray = dataArray
        # 每次传输的字节数
        self.byteNumPerSend = 65536
        self.finishFunctor = finishFunctor

    # 获取data array的指定片段
    def getDataArraySlice(self, idByte, byteNum):
        return getDataArraySlice(self.dataArray, idByte, byteNum)

    # 获取数据的个数
    def getDataLength(self):
        return len(self.dataArray)

# 用于接收long array的package
class LongArrayReceivePackage:
    def __init__(self,byteNum):
        self.byteNum
        self.dataArray = bytearray(byteNum)

    # 写入指定的片段
    def recordByteArray(self, writeArray, beginId):
        self.dataArray[beginId:beginId+len(writeArray)] = writeArray