import os
import shutil

def delete_folder(folder_path):
    """
    删除指定文件夹及其所有内容
    
    参数:
        folder_path (str): 要删除的文件夹路径
        
    返回:
        bool: 删除成功返回True，失败返回False
    """
    try:
        # 检查路径是否存在
        if not os.path.exists(folder_path):
            return False
        
        # 检查是否是文件夹
        if not os.path.isdir(folder_path):
            print(f"错误：'{folder_path}' 不是文件夹")
            return False
        
        # 递归删除文件夹
        shutil.rmtree(folder_path)
        print(f"成功删除文件夹: {folder_path}")
        return True
    
    except Exception as e:
        print(f"删除失败: {str(e)}")
        return False


def mkdir_p(path):
    """
    递归创建目录（类似Unix的mkdir -p命令）
    
    参数:
        path (str): 要创建的目录路径
        
    返回:
        bool: 创建成功返回True，失败返回False
    """
    try:
        # 使用os.makedirs创建目录，exist_ok=True表示目录存在时不报错
        os.makedirs(path, exist_ok=True)
        print(f"成功创建目录: {path}")
        return True
    except Exception as e:
        print(f"创建目录失败: {str(e)}")
        return False

def read_file_to_bytearray(file_path, verbose=False):
    """
    增强版文件读取函数
    
    参数:
        file_path (str): 文件路径
        verbose (bool): 是否显示详细操作信息
        
    返回:
        bytearray: 文件内容的bytearray
        None: 读取失败时返回
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        # 检查是否为文件
        if not os.path.isfile(file_path):
            raise IsADirectoryError(f"路径是目录而不是文件: {file_path}")
        
        # 检查文件大小（防止读取超大文件）
        file_size = os.path.getsize(file_path)
        if verbose:
            print(f"准备读取文件: {file_path} ({file_size} 字节)")
        
        # 设置读取限制（例如100MB）
        MAX_SIZE = 100 * 1024 * 1024  # 100MB
        if file_size > MAX_SIZE:
            raise MemoryError(f"文件过大 ({file_size} 字节 > {MAX_SIZE} 字节限制)")
        
        # 读取文件
        with open(file_path, 'rb') as file:
            content = file.read()
            
            if verbose:
                print(f"成功读取 {len(content)} 字节")
                
            return bytearray(content)
    
    except Exception as e:
        if verbose:
            print(f"错误: {str(e)}", file=sys.stderr)
        return None
    
def save_bytearray_to_file(data: bytearray, file_path: str) -> None:
    """
    将bytearray数据保存为二进制文件
    
    参数:
        data: bytearray类型的数据
        file_path: 文件保存路径（字符串）
    
    返回:
        None
    """
    with open(file_path, 'wb') as file:
        file.write(data)