from PIL import Image
import numpy as np

def saveTextureAsImage(texture: np.ndarray, imagePath: str):
    # 确保输入是3通道的RGB图像
    if texture.ndim != 3 or texture.shape[2] != 3:
        raise ValueError("Input texture must be 3-channel RGB array with shape [H, W, 3]")
    
    # 处理浮点数类型（假设范围[0,1]或[0,255]）
    if np.issubdtype(texture.dtype, np.floating):
        texture = np.clip(texture, 0, 255)  # 处理溢出
        texture = (texture * 255).astype(np.uint8)  # 确保是uint8
    
    # 处理整数类型（非uint8）
    elif texture.dtype != np.uint8:
        texture = np.clip(texture, 0, 255).astype(np.uint8)
    
    # 创建并保存图像
    img = Image.fromarray(texture, 'RGB')
    img.save(imagePath)

def convertToUIntFormat(image: np.ndarray) -> np.ndarray:
    """
    将float/np.float32格式的图片转换到[0,255]范围的uint8格式
    输入类型：uint8或float（任意范围）
    """
    # 如果是uint8类型直接返回
    if image.dtype == np.uint8:
        return image
        
    # 处理浮点数类型
    if np.issubdtype(image.dtype, np.floating):
        # 识别常见数据范围并自动转换
        img_min = np.min(image)
        img_max = np.max(image)
        
        if img_min >= 0:  # 非负值
            if img_max <= 1.0:  # 典型的[0,1]范围
                return (image * 255).clip(0, 255).astype(np.uint8)
            elif img_max <= 255:  # 已经是[0,255]范围
                return image.clip(0, 255).astype(np.uint8)
                
        # 处理其他范围或带负值的情况
        normalized = (image - img_min) / (img_max - img_min + 1e-8)
        return (normalized * 255).clip(0, 255).astype(np.uint8)
    
    # 处理非浮点数类型（如int16等）
    # 获取数据类型的数值范围
    dtype = image.dtype
    dtype_min = np.iinfo(dtype).min
    dtype_max = np.iinfo(dtype).max
    
    # 线性映射到[0,255]
    normalized = (image.astype(np.float32) - dtype_min) / (dtype_max - dtype_min)
    return (normalized * 255).clip(0, 255).astype(np.uint8)