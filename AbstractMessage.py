from StreamInterface import StreamInterface
from MessageManager import MessageManager

# 抽象的消息信息
class AbstractMessage:
    def __init__(self, name:str):
        self.name = name

    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream:StreamInterface):
        pass

    def receive(self, stream:StreamInterface, messageManager:MessageManager):
        pass