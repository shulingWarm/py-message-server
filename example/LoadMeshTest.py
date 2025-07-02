import sys
sys.path.append("/mnt/data/workspace/socket_server")

from TriMeshSolver import TriMeshSolver

meshPath = '/mnt/data/temp/car.ply'
mesh = TriMeshSolver(meshPath)

print(type(mesh.mesh.faces))
print(mesh.mesh.faces)
print(len(mesh.mesh.faces))

# 打印mesh里面节点的个数
# print(mesh.getVertexNum())
