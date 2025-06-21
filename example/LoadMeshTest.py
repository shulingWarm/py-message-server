import sys
sys.path.append("/mnt/data/workspace/socket_server")

from TriMeshSolver import TriMeshSolver

meshPath = '/mnt/data/temp/car.ply'
mesh = TriMeshSolver(meshPath)

# 打印mesh里面节点的个数
print(mesh.getVertexNum())
