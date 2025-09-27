from ModelLoadManager import ModelLoader, get_model_manager
from diffusers import QwenImageEditPipeline
from diffusers.utils import load_image

from nunchaku import NunchakuQwenImageTransformer2DModel
import torch
import gc

class ImageEditPipeline(ModelLoader):
    def __init__(self,
                 transformer_path:str,
                 model_path:str
    ):
        super('ImageEditPipeline', 30*1024*1024*1024)
        self.transformer_path = transformer_path
        self.model_path = model_path

    def __call__(self, image, prompt):
        # 执行推理过程
        output = self.pipeline(image=image, prompt=prompt, true_cfg_scale=4.0,
                               negative_prompt="", num_inference_steps=50)
        return output

    # 执行加载模型
    # 交由子类实现
    def load_model(self):
        # 加载transformer模型
        self.transformer = NunchakuQwenImageTransformer2DModel.from_pretrained(
            self.transformer_path, device='cuda', offload=False
        )

        self.pipeline = QwenImageEditPipeline.from_pretrained(
            self.model_path, transformer=self.transformer, torch_dtype=torch.bfloat16,
            device_map='cuda'
        )

    # 释放模型的内存
    # 交由子类实现
    def release_model(self):
        del self.transformer
        del self.pipeline
        self.transformer = None
        self.pipeline = None

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
    
def register_image_edit_pipeline():
    manager = get_model_manager()
    transformer_path = '/mnt/data/models/nunchaku_qwen_image_edit/svdq-int4_r128-qwen-image-edit.safetensors'
    qwen_image_edit_path = '/mnt/data/models/Qwen/Qwen-Image-Edit'
    manager.registerModel(ImageEditPipeline(
        transformer_path=transformer_path,
        model_path=qwen_image_edit_path
    ))