from AbstractMessage import AbstractMessage

class HelloMessage(AbstractMessage):
    def __init__(self):
        super().__init__('HelloMessage')
        
    # 消息的发送逻辑
    # 需要根据数据流来发送
    def send(self, stream):
        # 通过stream发送字符串
        stream.writeUTF('Hello from linux')

    def receive(self, stream, messageManager):
        # 接收文本信息
        # 这个flag会被弃用
        messageText = stream.readUTF()
        # 打印接收到的消息
        print('收到消息: ', messageText)