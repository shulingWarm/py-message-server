from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline
import sys
import os
# 插入hunyuan2.1的命名空间
sys.path.insert(0, '/mnt/data/code/Hunyuan3D-2.1/hy3dpaint')
from NoFilePipeline import NoFilePipeline
from ModelLoadManager import ModelLoader, get_model_manager
import gc
import torch

class MeshStruct:
    def __init__(self,vtx_pos, pos_idx, vtx_uv, uv_idx, texture_data, texture_metallic):
        self.vertexList = vtx_pos
        self.faceList = pos_idx
        self.vertexUvList = vtx_uv
        self.faceUvList = uv_idx
        self.textureData = texture_data
        self.textureMetallic = texture_metallic


class HunyuanTextureMeshPipeline(ModelLoader):
    def __init__(self,shapeModelPath,
        textureModelPath
    ):
        super().__init__(vram_cost=25*1024*1024*1024, name="HunyuanTextureMeshPipeline")
        self.shapeModelPath = shapeModelPath
        self.shape_pipeline = None
        self.texture_pipeline = None
        

    # 执行加载模型
    # 交由子类实现
    def load_model(self):
        # 加载shape model
        self.shape_pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_single_file(
            ckpt_path=os.path.join(self.shapeModelPath, 'model.fp16.ckpt'),
            config_path=os.path.join(self.shapeModelPath, 'config.yaml'))
        # 加载纹理模型
        self.texture_pipeline = NoFilePipeline(
            checkpointPath = '/mnt/data/code/Hunyuan3D-2.1/ckpt/RealESRGAN_x4plus.pth',
            configPath = '/mnt/data/code/Hunyuan3D-2.1/cfgs/hunyuan-paint-pbr.yaml',
            modelPath = '/mnt/data/models/Hunyuan3D-2.1',
            customPipeline = '/mnt/data/code/Hunyuan3D-2.1/hy3dpaint/hunyuanpaintpbr'
        )

    # 释放模型的内存
    # 交由子类实现
    def release_model(self):
        del self.shape_pipeline
        del self.texture_pipeline
        self.shape_pipeline = None
        self.texture_pipeline = None

        # 执行垃圾回收
        gc.collect()
        
        # 3. 清空PyTorch缓存
        torch.cuda.empty_cache()
        
        # 4. 重置CUDA上下文
        if torch.cuda.is_available():
            torch.cuda.synchronize()
            torch.cuda.reset_peak_memory_stats()
            torch.cuda.reset_accumulated_memory_stats()

    # 获取模型的实体
    # 具体返回什么类型由子类决定
    def get_model_instance(self):
        return self

    def __call__(self,image):
        # 将image输入到shape pipeline里面
        mesh = self.shape_pipeline(image=image)[0]
        # 对mesh做降采样
        mesh = mesh.simplify_quadric_decimation(face_count=40000)
        # 把mesh输入到纹理模型里面
        vtx_pos, pos_idx, vtx_uv, uv_idx, texture_data, texture_metallic = self.texture_pipeline.generate(image=image, mesh=mesh)
        # 返回一个包装过的mesh形式
        return MeshStruct(vtx_pos, pos_idx, vtx_uv, uv_idx, texture_data, texture_metallic)

def register_hunyuan_pipeline():
    manager = get_model_manager()
    manager.registerModel(HunyuanTextureMeshPipeline('/mnt/data/models/Hunyuan3D_dit_v2',
            '/mnt/data/models/Hunyuan3D-2.1'))