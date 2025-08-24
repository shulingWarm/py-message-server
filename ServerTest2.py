from MessageManager import MessageManager
from SocketSolver import SocketSolver
from HelloMessage import HelloMessage
from ImageMessage import ImageMessage
from ImageEndMessage import ImageEndMessage
from ImageReceiveMessage import ImageReceiveMessage
from ImageRowData import ImageRowData
from HunyuanMeshGenMessage import HunyuanMeshGenMessage
from MeshGenServer import MeshGenServer
from MeshMessage import MeshMessage
from RequestMeshVertices import RequestMeshVertices
from VertexFinishMessage import VertexFinishMessage
from VertexArrayBack import VertexArrayBack
from MeshTestMessage import MeshTestMessage
from RequestFaceMessage import RequestFaceMessage
from FaceArrayBack import FaceArrayBack
from FinishFaceMessage import FinishFaceMessage
from LongArrayMessage import LongArrayMessage
from RequestLongArrayMessage import RequestLongArrayMessage, staticLongArrayRequest
from LongArrayBackMessage import LongArrayBackMessage
from UvVertexFinishMessage import UvVertexFinishMessage
from RequestTextureMessage import RequestTextureMessage
from TextureFinishMessage import TextureFinishMessage
from RequestFaceUvMessage import RequestFaceUvMessage
from FaceUvFinishMessage import FaceUvFinishMessage
import MessageLoop

# 默认的端口号
port = 23456

# 初始化mesh gen的server
MeshGenServer.serverInstance = MeshGenServer()

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
manager.registerMessage(HunyuanMeshGenMessage())
manager.registerMessage(MeshMessage(None, 0, 0))
manager.registerMessage(VertexArrayBack(None, 0, 0))
manager.registerMessage(VertexFinishMessage(0))
manager.registerMessage(RequestMeshVertices())
manager.registerMessage(MeshTestMessage())
manager.registerMessage(RequestFaceMessage())
manager.registerMessage(FaceArrayBack(0,0,None))
manager.registerMessage(FinishFaceMessage(0))
manager.registerMessage(LongArrayMessage(None, None))
manager.registerMessage(RequestLongArrayMessage())
manager.registerMessage(LongArrayBackMessage(0,0,None, staticLongArrayRequest))
manager.registerMessage(UvVertexFinishMessage(0))
manager.registerMessage(RequestTextureMessage())
manager.registerMessage(TextureFinishMessage(0))
manager.registerMessage(RequestFaceUvMessage())
manager.registerMessage(FaceUvFinishMessage(0))

# 启动solver的监听过程
solver.listen(port)

# 启动主线程
thread = MessageLoop.startLoop(manager, solver)
# python里面不要考虑多线程的事，会严重影响性能的
thread.join()
