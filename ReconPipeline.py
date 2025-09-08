import sys
sys.path.insert(0, '/mnt/data/code/vggt-low-vram')
sys.path.insert(0, '/mnt/data/code/gaussian-splatting')
from callable_pipeline import ReconstructionPipeline
from train_pipeline import GaussianTrainPipeline
import os
import FileLib

# 执行三维重建的pipeline 最后生成出来的是3DGS
class ReconPipeline:
    def __init__(self):
        # 加载vggt的pipeline
        self.vggt_pipeline = ReconstructionPipeline()
        self.gs_pipeline = GaussianTrainPipeline()

    # 执行重建
    def run(self, scene_path):
        # 删除scene里面的sparse目录
        sparse_path = os.path.join(scene_path, 'sparse')
        FileLib.delete_folder(sparse_path)
        # 执行vggt的重建
        self.vggt_pipeline.run(scene_path)
        # 执行gaussian splatting
        self.gs_pipeline.run(scene_path)
        # 计算splat文件的路径
        splat_file_path = os.path.join(scene_path, 'splat.ply')
        return splat_file_path


reconPipeInstance = None

def getReconInstance():
    global reconPipeInstance
    if(reconPipeInstance is None):
        reconPipeInstance = ReconPipeline()
    return reconPipeInstance
    