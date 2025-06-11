
# 抽象的消息信息
class AbstractMessage:
    def __init__(self, name:str):
        self.name = name
        # message的数据头


    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream):
        pass

    def receive(self, stream, messageManager):
        pass