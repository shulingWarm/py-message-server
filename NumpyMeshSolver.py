from MeshSolver import MeshSolver
import numpy as np

class NumpyMeshSolver(MeshSolver):
    def __init__(self,
        vertices: np.ndarray,        # shape: [vertex_num, 3]
        faceList: np.ndarray,         # shape: [face_num, 3]
        vertexUv: np.ndarray,        # shape: [vertex_num, 2]
        faceUvIndex: np.ndarray,      # shape: [face_num, 3]
        textureData: np.ndarray,      # shape: [H, W, 3]
        textureMetallic: np.ndarray   # shape: [H, W, 3]
    ):
        # 初始化所有数据为只读属性，防止意外修改
        self._vertices = vertices.view()
        self._faceList = faceList.view()
        self._vertexUv = vertexUv.view()
        self._faceUvIndex = faceUvIndex.view()
        self._textureData = textureData.view()
        self._textureMetallic = textureMetallic.view()
        
        # 将数组设置为只读
        for arr in [self._vertices, self._faceList, self._vertexUv, 
                    self._faceUvIndex, self._textureData, self._textureMetallic]:
            arr.flags.writeable = False
    
    # 获取总的节点个数
    def getVertexNum(self) -> int:
        return self._vertices.shape[0]

    # 获取连续顶点序列 [x0,y0,z0, x1,y1,z1,...]
    def getVertexArray(self, vertexId: int, vertexNum: int) -> list:
        # 计算有效提取范围
        end_idx = min(vertexId + vertexNum, self._vertices.shape[0])
        valid_num = end_idx - vertexId
        
        # 提取并展平顶点数据
        data = self._vertices[vertexId:vertexId+valid_num]
        flattened = data.ravel().tolist()
        
        # 不足部分填充0
        if valid_num < vertexNum:
            flattened += [0] * (3 * (vertexNum - valid_num))
        return flattened

    # 获取face的个数
    def getMeshFaceNum(self) -> int:
        return self._faceList.shape[0]

    # 获取连续面序列 [f00,f01,f02, f10,f11,f12,...]
    def getFaceArray(self, faceId: int, faceNum: int) -> list:
        # 计算有效提取范围
        end_idx = min(faceId + faceNum, self._faceList.shape[0])
        valid_num = end_idx - faceId
        
        # 提取并展平面索引
        data = self._faceList[faceId:faceId+valid_num]
        flattened = data.ravel().tolist()
        
        # 不足部分填充-1
        if valid_num < faceNum:
            flattened += [-1] * (3 * (faceNum - valid_num))
        return flattened

    # 获取纹理尺寸 (宽, 高)
    def getTextureDataSize(self) -> tuple:
        return (self._textureData.shape[1], self._textureData.shape[0])  # (width, height)

    # 获取连续纹理像素 [r0,g0,b0, r1,g1,b1,...]
    def getTextureData(self, pixelId: int, pixelNum: int) -> list:
        total_pixels = self._textureData.size // 3
        
        # 计算有效的像素提取范围
        end_idx = min(pixelId + pixelNum, total_pixels)
        valid_num = end_idx - pixelId
        
        # 计算像素在二维数组中的位置
        width = self._textureData.shape[1]
        start_row = pixelId // width
        start_col = pixelId % width
        end_row = (end_idx - 1) // width
        end_col = (end_idx - 1) % width
        
        # 提取像素数据
        if start_row == end_row:
            # 单行提取
            pixels = self._textureData[start_row, start_col:start_col+valid_num]
        else:
            # 跨行提取
            first_row = self._textureData[start_row, start_col:]
            middle_rows = self._textureData[start_row+1:end_row].reshape(-1, 3)
            last_row = self._textureData[end_row, :end_col+1]
            pixels = np.vstack((first_row, middle_rows, last_row))
        
        # 返回展平数据
        return pixels.ravel().tolist()

    # 获取连续金属贴图像素（实现与getTextureData相同）
    def getMetallicData(self, pixelId: int, pixelNum: int) -> list:
        total_pixels = self._textureMetallic.size // 3
        end_idx = min(pixelId + pixelNum, total_pixels)
        valid_num = end_idx - pixelId
        
        width = self._textureMetallic.shape[1]
        start_row = pixelId // width
        start_col = pixelId % width
        end_row = (end_idx - 1) // width
        end_col = (end_idx - 1) % width
        
        if start_row == end_row:
            pixels = self._textureMetallic[start_row, start_col:start_col+valid_num]
        else:
            first_row = self._textureMetallic[start_row, start_col:]
            middle_rows = self._textureMetallic[start_row+1:end_row].reshape(-1, 3)
            last_row = self._textureMetallic[end_row, :end_col+1]
            pixels = np.vstack((first_row, middle_rows, last_row))
        
        return pixels.ravel().tolist()