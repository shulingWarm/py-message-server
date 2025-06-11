import SocketSolver

solver = SocketSolver.SocketSolver()
solver.setLocalAsServer(23456)

# 读取int数据
numData = solver.readInt()
# 打印接收到的数据
print(numData)
# 返回接收到的数据
solver.writeInt(321)

while(True):
    pass