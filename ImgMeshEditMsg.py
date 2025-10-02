from AbstractMessage import AbstractMessage
from StreamInterface import StreamInterface
from MessageManager import MessageManager
from ModelLoadManager import get_model_manager
from MeshGenServer import MeshGenServer
from HunyuanMeshGenMessage import MeshFinishCallback

# 对图片做编辑的消息
class ImgMeshEditMsg(AbstractMessage):
    def __init__(self):
        super().__init__('ImgMeshEditMsg')

    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream:StreamInterface):
        pass

    def receive(self, stream:StreamInterface, messageManager:MessageManager):
        # 接收图片的id
        imgIdPkg = stream.readUInt()
        # 接收图片的id
        meshTaskId = stream.readUInt()
        # 读取提示词
        prompt = stream.readUTF()
        # 从包管理器里面读取图片
        imagePackage = stream.getPackageManager().getRemotePackage(imgIdPkg)
        # 从package里面把图片本体拿出来
        image = imagePackage.image
        model_manager = get_model_manager()
        # 获取图片编辑模型
        imgEditPipeline = model_manager.get_model('ImageEditPipeline')
        # 调用图片先编辑再生成Mesh的流程
        editedImg = imgEditPipeline(image=image, prompt=prompt)
        del imgEditPipeline
        imgEditPipeline = None
        # 获取hunyuan 生成mesh的模型
        meshGenPipeline = MeshGenServer.serverInstance
        # 通过图片调用edit流程
        meshGenPipeline.generateMesh(editedImg,
            MeshFinishCallback(messageManager, imgIdPkg, idTaskPackage=meshTaskId))