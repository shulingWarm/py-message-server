from AbstractMessage import AbstractMessage
import ReconPipeline
from LongArrayFinishFunctor import LongArrayFinishFunctor
from ReconResultMsg import ReconResultMsg
import FileCommLib

# 重建完成时的functor
# 用于通知UE已经发送完了重建完成的消息
class ReconLongArrayEndFunctor(LongArrayFinishFunctor):
    # requestIdPackage 用来记录当时的重建请求
    def __init__(self,requestIdPackage):
        self.requestIdPackage = requestIdPackage

    # 执行函数
    def __call__(self,messageManager, idPackage):
        # 新建用于发送重建结果的消息
        resultMsg = ReconResultMsg(idPackage, self.requestIdPackage)
        messageManager.sendMessage(resultMsg)

class ReconBeginMsg(AbstractMessage):
    def __init__(self):
        super().__init__('ReconBeginMsg')

    def send(self, stream):
        pass

    def receive(self, stream, messageManager):
        idPackage = stream.readUInt()
        # 接收重建包的id
        reconPkg = stream.getPackageManager().getRemotePackage(idPackage)
        # 重建接收包可以就此删除了
        stream.getPackageManager().deleteRemotePackage(idPackage)
        # 用于重建的pipeline
        reconPipeline = ReconPipeline.getReconInstance()
        # 开始执行重建
        resultPath = reconPipeline.run(reconPkg.scene_path)
        # 回调消息，用于发送完成重建结果的事情
        finishFunctor = ReconLongArrayEndFunctor(idPackage)
        # 执行发送文件的逻辑
        FileCommLib.sendFile(resultPath, messageManager, finishFunctor)
        
    