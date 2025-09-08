import socket
import struct
from PackageMsgManager import PackageMsgManager
from StreamInterface import StreamInterface

class SocketSolver(StreamInterface):
    def __init__(self):
        self.server_socket = None
        self.client_socket = None
        self.client_address = None
        #solver里面的消息分包管理器
        self.packageManager = PackageMsgManager()
        # 每种数据类型的字节数
        self.typeByteSizeMap = {
            'int':4,
            'uint':4,
            'float':4,  # 单精度浮点数占4字节
            'double':8  # 双精度浮点数占8字节
        }
        # 每种数据类型对应的unpack符号
        self.typePackSymbol = {
            'int':'<i',
            'uint':'<I',
            'float':'<f',  # 单精度浮点数格式符
            'double':'<d'  # 双精度浮点数格式符
        }

    def listen(self, port: int):
        # 关闭现有连接（如果有）
        if self.client_socket:
            self.client_socket.close()
        if self.server_socket:
            self.server_socket.close()
            
        # 创建TCP套接字
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置地址重用选项，避免端口占用问题
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            # 绑定到所有接口的指定端口
            self.server_socket.bind(('0.0.0.0', port))
            # 开始监听，设置最大连接数为1
            self.server_socket.listen(1)
            print(f"Listening on port {port}...")
            
            # 阻塞直到客户端连接
            self.client_socket, self.client_address = self.server_socket.accept()
            print(f"Client connected from: {self.client_address}")
            
        except Exception as e:
            self.server_socket.close()
            raise RuntimeError(f"Listen failed: {str(e)}")

    def readData(self, byteSize: int) -> bytearray:
        if not self.client_socket:
            raise RuntimeError("No active connection. Call listen() first.")
        
        data = bytearray()
        try:
            # 循环读取直到达到指定字节数
            while len(data) < byteSize:
                packet = self.client_socket.recv(byteSize - len(data))
                if not packet:  # 连接关闭
                    raise ConnectionError("Connection closed by client")
                data.extend(packet)
            return data
            
        except Exception as e:
            self.client_socket.close()
            self.client_socket = None
            raise RuntimeError(f"Read operation failed: {str(e)}")

    def writeData(self, data: bytearray):
        if not self.client_socket:
            raise RuntimeError("No active connection. Call listen() first.")
        
        try:
            total_sent = 0
            # 确保发送所有数据
            while total_sent < len(data):
                sent = self.client_socket.send(data[total_sent:])
                if sent == 0:  # 连接已断开
                    raise ConnectionError("Socket connection broken")
                total_sent += sent
                
        except Exception as e:
            self.client_socket.close()
            self.client_socket = None
            raise RuntimeError(f"Write operation failed: {str(e)}")
    
    # 根据数据类型决定字节长度
    def getTypeByteSize(self, dataType):
        # 判断数据类型是否有记录
        if dataType not in self.typeByteSizeMap:
            raise RuntimeError(f'Unknown type: {dataType}')
        # 返回字节数的查找结果
        return self.typeByteSizeMap[dataType]

    # 根据数据类型获取编解码时的symbol
    def getTypeSymbol(self, dataType):
        # 判断数据类型是否有记录
        if dataType not in self.typePackSymbol:
            raise RuntimeError(f'Unknown type: {dataType}')
        return self.typePackSymbol[dataType]

    # 根据数据类型来读取
    def readType(self, dataType):
        # 读取字节流
        byteData = self.readData(self.getTypeByteSize(dataType))
        # 根据类型做unpack
        return struct.unpack(self.getTypeSymbol(dataType), byteData)[0]

    # 根据数据类型写入数据
    def writeType(self, dataType, value):
        # 将数据转换成字节流
        byteData = struct.pack(self.getTypeSymbol(dataType), value)
        # 将数据发送出去
        self.writeData(byteData)

    def readArray(self, dataType, size):
        # 获取单元素的struct格式符（带字节序）
        typeSymbol = self.getTypeSymbol(dataType)
        # 拆分字节序符号和类型符号
        endian_symbol = typeSymbol[0]  # 第一个字符是字节序（'<' 或 '>'）
        base_symbol = typeSymbol[1:]   # 剩余部分是基础类型符（如 'i', 'I'）
        
        # 创建完整的数组格式符（字节序 + 元素个数 + 基础类型符）
        arrayFormat = f"{endian_symbol}{size}{base_symbol}"
        # 计算需要读取的总字节数
        elementByteSize = self.getTypeByteSize(dataType)
        totalBytes = elementByteSize * size
        
        # 读取整个数组的数据
        byteData = self.readData(totalBytes)
        # 一次性解包整个数组
        return list(struct.unpack(arrayFormat, byteData))

    def writeArray(self, dataType, dataList):
        # 获取单元素的struct格式符（带字节序）
        typeSymbol = self.getTypeSymbol(dataType)
        # 拆分字节序符号和类型符号
        endian_symbol = typeSymbol[0]  # 第一个字符是字节序（'<' 或 '>'）
        base_symbol = typeSymbol[1:]   # 剩余部分是基础类型符（如 'i', 'I'）
        
        # 创建完整的数组格式符（字节序 + 元素个数 + 基础类型符）
        arrayFormat = f"{endian_symbol}{len(dataList)}{base_symbol}"
        # 一次性打包整个列表
        byteData = struct.pack(arrayFormat, *dataList)
        # 发送打包后的字节数据
        self.writeData(bytearray(byteData))

    # 写入字符串
    def writeUTF(self, message):
        # 把字符串编码成字节数据
        byteData = message.encode('utf-8')
        # 先写入字符串的长度
        self.writeType('uint', len(byteData))
        # 写入编码过的数据信息
        self.writeData(byteData)

    # 读取字符串
    def readUTF(self):
        # 读取字符串的长度
        strLength = self.readType('uint')
        # 根据长度读取字符串信息
        byteData = self.readData(strLength)
        # 对信息做解码得到字符串
        return byteData.decode('utf-8')

    # 读取无符号整型
    def readUInt(self):
        return self.readType('uint')

    def readInt(self):
        return self.readType('int')
    
    def writeUInt(self, value):
        self.writeType('uint', int(value))

    def writeInt(self, value):
        self.writeType('int', int(value))

    # 获得分包管理器
    def getPackageManager(self):
        return self.packageManager