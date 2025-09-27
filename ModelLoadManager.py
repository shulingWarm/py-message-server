import torch

# 这里面用于管理模型加载和卸载的功能

# 基本的模型加载功能
class ModelLoader:
    def __init__(self, name, vram_cost):
        self.name = name
        self.vram_cost = vram_cost

    # 执行加载模型
    # 交由子类实现
    def load_model(self):
        pass

    # 释放模型的内存
    # 交由子类实现
    def release_model(self):
        pass

    # 获取模型的实体
    # 具体返回什么类型由子类决定
    def get_model_instance(self):
        pass

class ModelLoadManager:
    def __init__(self, total_vram: int):
        self.loader_dict = {}
        self.total_vram = total_vram
        self.current_vram_usage = 0
        self.loaded_models = {}  # 存储已加载模型的名称和对应的loader
        self.access_order = []   # 记录模型访问顺序（LRU策略）

    def registerModel(self, loader: ModelLoader):
        self.loader_dict[loader.name] = loader

    def get_model(self, model_name: str):
        # 检查模型是否已注册
        if model_name not in self.loader_dict:
            raise KeyError(f"Model '{model_name}' is not registered")

        loader = self.loader_dict[model_name]
        
        # 如果模型已加载，更新访问顺序并返回
        if model_name in self.loaded_models:
            self.access_order.remove(model_name)
            self.access_order.append(model_name)
            return loader.get_model_instance()
        
        # 检查模型是否超过总VRAM容量
        if loader.vram_cost > self.total_vram:
            raise ValueError(
                f"Model '{model_name}' requires {loader.vram_cost} bytes VRAM, "
                f"exceeding total system VRAM ({self.total_vram} bytes)"
            )
        
        # 释放其他模型直到有足够空间
        while self.current_vram_usage + loader.vram_cost > self.total_vram:
            if not self.access_order:
                raise RuntimeError(
                    f"Insufficient VRAM to load model '{model_name}' "
                    f"(requires {loader.vram_cost} bytes), "
                    f"no more models to release"
                )
            
            # 释放最近最少使用的模型
            lru_model = self.access_order.pop(0)
            lru_loader = self.loaded_models.pop(lru_model)
            lru_loader.release_model()
            self.current_vram_usage -= lru_loader.vram_cost
        
        # 加载新模型
        loader.load_model()
        self.loaded_models[model_name] = loader
        self.access_order.append(model_name)
        self.current_vram_usage += loader.vram_cost
        
        return loader.get_model_instance()


# 模型加载的管理器
free_mem, total_mem = torch.cuda.mem_get_info('cuda')
local_manager = ModelLoadManager(free_mem)

# 获取本地的manager
def get_model_manager() -> ModelLoadManager:
    global local_manager
    return local_manager