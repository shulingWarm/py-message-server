from abc import ABC, abstractmethod
from PackageMsgManager import PackageMsgManager

class StreamInterface(ABC):
    def __init__(self):
        # 子类应初始化以下属性：
        # self.server_socket = None
        # self.client_socket = None
        # self.client_address = None
        # self.packageManager = PackageMsgManager()
        # self.typeByteSizeMap = {...}
        # self.typePackSymbol = {...}
        pass

    @abstractmethod
    def listen(self, port: int):
        """启动服务器监听指定端口"""
        pass

    @abstractmethod
    def readData(self, byteSize: int) -> bytearray:
        """从连接中读取指定字节数的数据"""
        pass

    @abstractmethod
    def writeData(self, data: bytearray):
        """向连接写入字节数据"""
        pass

    @abstractmethod
    def getTypeByteSize(self, dataType: str) -> int:
        """获取指定数据类型对应的字节大小"""
        pass

    @abstractmethod
    def getTypeSymbol(self, dataType: str) -> str:
        """获取指定数据类型对应的struct打包符号"""
        pass

    @abstractmethod
    def readType(self, dataType: str):
        """根据数据类型读取单个值"""
        pass

    @abstractmethod
    def writeType(self, dataType: str, value):
        """根据数据类型写入单个值"""
        pass

    @abstractmethod
    def readArray(self, dataType: str, size: int) -> list:
        """读取指定类型和大小的数组"""
        pass

    @abstractmethod
    def writeArray(self, dataType: str, dataList: list):
        """写入指定类型的数组"""
        pass

    @abstractmethod
    def writeUTF(self, message: str):
        """写入UTF-8编码的字符串"""
        pass

    @abstractmethod
    def readUTF(self) -> str:
        """读取UTF-8编码的字符串"""
        pass

    @abstractmethod
    def readUInt(self) -> int:
        """读取无符号整型"""
        pass

    @abstractmethod
    def readInt(self) -> int:
        """读取有符号整型"""
        pass

    @abstractmethod
    def writeUInt(self, value: int):
        """写入无符号整型"""
        pass

    @abstractmethod
    def writeInt(self, value: int):
        """写入有符号整型"""
        pass

    # 获得分包管理器
    def getPackageManager(self) -> PackageMsgManager:
        return self.packageManager