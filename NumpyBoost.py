import numpy

# 这里面会实现一些numpy的扩展库
import numpy as np

def getNumpyByteArray(npData):
    """
    将NumPy数组转换为bytearray，自动处理连续性和数据类型
    
    参数:
        npData (np.ndarray): 输入NumPy数组
        
    返回:
        bytearray: 表示数组原始内存布局的字节数组
        
    处理过程:
        1. 确保数组是内存连续的
        2. 保留原始数据类型和字节序
        3. 返回数组的原始字节表示
    """
    # 检查数组是否连续（内存布局）
    if not npData.flags.c_contiguous:
        # 非连续则创建连续副本（不改变原始数组）
        npData = np.ascontiguousarray(npData)
    
    # 获取数组原始字节表示
    byte_arr = bytearray(npData.data)
    
    return byte_arr