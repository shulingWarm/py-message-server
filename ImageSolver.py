from PIL import Image

class ImageSolver:
    def __init__(self, imgWidth, imgHeight):
        # 创建全透明背景的RGBA图像
        self.width = imgWidth
        self.height = imgHeight
        self.img = Image.new("RGBA", (imgWidth, imgHeight), (0, 0, 0, 0))
        self.pixels = self.img.load()  # 获取像素访问对象

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
        