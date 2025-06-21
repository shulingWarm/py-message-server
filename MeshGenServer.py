from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline
import threading


# 定义Mesh后续处理的接口
class MeshPostProcessInterface:
    def __init__(self):
        pass

    # 对mesh数据类型做后处理
    # 这个东西要交给子类实现
    def meshProcess(self,mesh):
        pass

# 生成mesh的异步函数
def meshGenProcess(pipeline, image, meshPostProcess):
    # 调用生成mesh的过程
    mesh = pipeline(image=image)
    # 调用生成mesh后的过程
    meshPostProcess.meshProcess(mesh)

# 支持异步调用的Mesh生成逻辑
class MeshGenServer:
    # server的实例
    # 不算很严格的单例模式
    serverInstance = None

    def __init__(self):
        # hunyuan 3D的pipeline
        self.pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_single_file(
            ckpt_path='/mnt/data/models/Hunyuan3D_dit_v2/model.fp16.ckpt',
            config_path='/mnt/data/models/Hunyuan3D_dit_v2/config.yaml')

    # 根据传入的图片生成mesh
    def generateMesh(self, image, meshPostProcess):
        # 启动生成mesh的runner
        thread = threading.Thread(
            target=meshGenProcess,
            args=(self.pipeline, image, meshPostProcess)
        )
        # 启动线程
        thread.start()