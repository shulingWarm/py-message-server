from MessageManager import MessageManager
from SocketSolver import SocketSolver
from HelloMessage import HelloMessage
from ImageMessage import ImageMessage
from ImageEndMessage import ImageEndMessage
from ImageReceiveMessage import ImageReceiveMessage
from ImageRowData import ImageRowData
import MessageLoop

# 默认的端口号
port = 23456

# 新建SocketSolver
solver = SocketSolver()
# 新建消息管理器
manager = MessageManager(solver)
# 注册基本的hello message
manager.registerMessage(HelloMessage())
manager.registerMessage(ImageMessage(None))
manager.registerMessage(ImageReceiveMessage(0, 0))
manager.registerMessage(ImageEndMessage())
manager.registerMessage(ImageRowData(None,0,0,0))
# 启动solver的监听过程
solver.listen(port)

# 启动主线程
thread = MessageLoop.startLoop(manager, solver)

while(True):
    pass