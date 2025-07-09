from LongArrayFinishFunctor import LongArrayFinishFunctor

# 数组发送结束时的通用模板，直接发送指定的消息
class ArrayFinishMessageFunctor(LongArrayFinishFunctor):
    def __init__(self, message):
        self.message = message

    # 执行函数
    def __call__(self,messageManager, idPackage):
        self.message.setIdArrayPackage(idPackage)
        messageManager.sendMessage(self.message)