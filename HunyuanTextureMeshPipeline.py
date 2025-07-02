from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline
import sys
import os
# 插入hunyuan2.1的命名空间
sys.path.insert(0, '/mnt/data/code/Hunyuan3D-2.1/hy3dpaint')
from NoFilePipeline import NoFilePipeline

class MeshStruct:
    def __init__(self,vtx_pos, pos_idx, vtx_uv, uv_idx, texture_data, texture_metallic):
        self.vertexList = vtx_pos
        self.faceList = pos_idx
        self.vertexUvList = vtx_uv
        self.faceUvList = uv_idx
        self.textureData = texture_data
        self.textureMetallic = texture_metallic


class HunyuanTextureMeshPipeline:
    def __init__(self,shapeModelPath,
        textureModelPath
    ):
        # 加载shape model
        self.shape_pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_single_file(
            ckpt_path=os.path.join(shapeModelPath, 'model.fp16.ckpt'),
            config_path=os.path.join(shapeModelPath, 'config.yaml'))
        # 加载纹理模型
        self.texture_pipeline = NoFilePipeline(
            checkpointPath = '/mnt/data/code/Hunyuan3D-2.1/ckpt/RealESRGAN_x4plus.pth',
            configPath = '/mnt/data/code/Hunyuan3D-2.1/cfgs/hunyuan-paint-pbr.yaml',
            modelPath = '/mnt/data/models/Hunyuan3D-2.1',
            customPipeline = '/mnt/data/code/Hunyuan3D-2.1/hy3dpaint/hunyuanpaintpbr'
        )

    def __call__(self,image):
        # 将image输入到shape pipeline里面
        mesh = self.shape_pipeline(image=image)[0]
        # 对mesh做降采样
        mesh = mesh.simplify_quadric_decimation(face_count=40000)
        # 把mesh输入到纹理模型里面
        vtx_pos, pos_idx, vtx_uv, uv_idx, texture_data, texture_metallic = self.texture_pipeline.generate(image=image, mesh=mesh)
        # 返回一个包装过的mesh形式
        return MeshStruct(vtx_pos, pos_idx, vtx_uv, uv_idx, texture_data, texture_metallic)