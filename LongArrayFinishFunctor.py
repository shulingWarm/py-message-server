
# 长数组发送完之后的回调
# 这属于是一个抽象接口
class LongArrayFinishFunctor:
    def __init__(self):
        pass

    # 执行函数
    def __call__(self,messageManager, idPackage):
        pass