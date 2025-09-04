import os

# 用于重建的package
class ReconstructionPackage:
    def __init__(self, imageNum):
        # 记录图片的个数
        self.imageNum = imageNum
        self.scene_path = '/mnt/data/temp/kitchen_workspace'
        # 保存图片的文件夹
        self.save_image_path = os.path.join(scene_path,'images')
        # 目前已经存储过的图片数
        self.saved_img_num = 0

    # 注册需要用于重建的图片
    def rgstReconImg(self, img):
        # 调用图片的存储接口，其实就是把它保存在本地
        save_path = os.path.join(self.save_image_path, f'{self.saved_img_num}.jpg')
        img.save(save_path)
        # 递增图片个数
        self.saved_img_num = self.saved_img_num + 1
        if(self.saved_img_num > self.imageNum):
            raise RuntimeError(f'Invalid self.saved_img_num: {self.saved_img_num}/{self.imageNum}')

    