import os
import FileLib

# 用于重建的package
class ReconstructionPackage:
    def __init__(self, imageNum):
        # 记录图片的个数
        self.imageNum = imageNum
        self.scene_path = '/mnt/data/temp/kitchen_workspace'
        # 保存图片的文件夹
        self.save_image_path = os.path.join(self.scene_path,'images')
        # 清空用于保存图片的文件夹
        FileLib.clear_folder(self.save_image_path)
        # 目前已经存储过的图片数
        self.saved_img_num = 0
        # 每个数字对应的格式
        self.fmtList = ['none','jpg','png']

    # 递增图片的个数
    def increaseImgNum(self):
        # 递增图片个数
        self.saved_img_num = self.saved_img_num + 1
        if(self.saved_img_num > self.imageNum):
            raise RuntimeError(f'Invalid self.saved_img_num: {self.saved_img_num}/{self.imageNum}')

    # 注册需要用于重建的图片
    def rgstReconImg(self, img):
        # 调用图片的存储接口，其实就是把它保存在本地
        save_path = os.path.join(self.save_image_path, f'{self.saved_img_num}.jpg')
        img.save(save_path)
        self.increaseImgNum()
        
    # 注册文件格式的数据流
    def rgstReconImgByFile(self, imgArray:bytearray, imgFmt:int)->None:
        # 根据枚举获得后缀名
        fmtStr = self.fmtList[imgFmt]
        # 确定保存的路径
        save_path = os.path.join(self.save_image_path, f'{self.saved_img_num}.{fmtStr}')
        # 调用文件保存的逻辑
        FileLib.save_bytearray_to_file(imgArray, save_path)
        self.increaseImgNum()