from AbstractMessage import AbstractMessage
from TriMeshSolver import TriMeshSolver
from MeshMessage import MeshMessage

# mesh的测试消息，当收到这个消息后立刻开始发送消息
class MeshTestMessage(AbstractMessage):
    def __init__(self):
        super().__init__('MeshTestMessage')

    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream):
        pass

    def receive(self, stream, messageManager):
        print('收到mesh测试消息')
        # 加载mesh
        mesh = TriMeshSolver('/mnt/data/temp/car.ply')
        # 新建发送mesh的消息
        meshMessage = MeshMessage(mesh, 0)
        # 发送mesh message
        messageManager.sendMessage(meshMessage)