from MeshSolver import MeshSolver
import trimesh
import numpy as np

class TriMeshSolver(MeshSolver):
    def __init__(self, filePath: str):
        """传入文件路径加载mesh对象"""
        self.mesh = trimesh.load(filePath)  # 加载网格

    def getVertexNum(self) -> int:
        """返回顶点总数"""
        return len(self.mesh.vertices)

    def getVertexArray(self, vertexId: int, vertexNum: int) -> list:
        """
        获取连续的顶点坐标数组（平面列表格式）
        参数:
            vertexId: 起始顶点索引
            vertexNum: 需要获取的顶点数量
        返回:
            顶点坐标的平面列表格式 [x0, y0, z0, x1, y1, z1, ...]
        """
        total_vertices = self.getVertexNum()
        
        # 验证参数有效性
        if vertexId >= total_vertices or vertexId < 0 or vertexNum <= 0:
            return []
        
        # 计算实际可获取的顶点数量
        actual_num = min(vertexNum, total_vertices - vertexId)
        
        # 提取顶点数据并转换为平面列表格式
        vertices = self.mesh.vertices[vertexId:vertexId + actual_num]
        return vertices.flatten().tolist()  # 展平数组并转为列表

    