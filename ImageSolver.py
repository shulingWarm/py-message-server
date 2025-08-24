from PIL import Image

class ImageSolver:
    def __init__(self, imgWidth, imgHeight, imgData=None):
        # 创建全透明背景的RGBA图像
        self.width = imgWidth
        self.height = imgHeight
        if(imgData is None):
            self.img = Image.new("RGBA", (imgWidth, imgHeight), (0, 0, 0, 0))
            self.pixels = self.img.load()  # 获取像素访问对象
        else:
            self.setAllPixel(imgData)

    # 设置所有的pixel信息
    # 需要确保传入的bytearray长度等于图片所有的像素数
    def setAllPixel(self, imgData: bytearray):
        # 计算预期的字节长度（宽×高×4个通道）
        expected_length = self.width * self.height * 4
        if len(imgData) != expected_length:
            raise ValueError(
                f"数据长度错误。需要 {expected_length} 字节，实际收到 {len(imgData)} 字节"
            )
        
        # 使用原始字节数据直接重建图像
        self.img = Image.frombytes('RGBA', (self.width, self.height), bytes(imgData))
        # 更新像素访问对象以保持一致性
        self.pixels = self.img.load()

    def setRowPixel(self, idRow, rowData):
        if idRow < 0 or idRow >= self.height:
            raise ValueError(f"行索引超出范围，有效范围0-{self.height-1}")
        
        # 验证数据长度（4字节RGBA * 宽度）
        expected_length = self.width * 4
        if len(rowData) != expected_length:
            raise ValueError(
                f"行数据长度错误。应为{expected_length}字节，实际为{len(rowData)}字节")
        
        # 逐像素设置数据
        for col in range(self.width):
            start = col * 4
            r, g, b, a = rowData[start:start+4]
            self.pixels[col, idRow] = (r, g, b, a)

    def save(self, filePath):
        # 自动根据文件扩展名选择格式
        self.img.save(filePath)
        
    # 获得底层的pil image
    def getImageImpl(self):
        return self.img