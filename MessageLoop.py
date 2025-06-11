import threading

# 在这个文件里面处理接收消息的主循环
# 消息的主循环函数
# 分别传入消息管理器和网络通信流
def messageLoop(manager, stream):
    print('消息循环开始')
    while True:
        # 从stream里面接收一个信息
        tag = stream.readUInt()
        # 判断tag是否在范围内
        if manager.isTagInRange(tag):
            # 告知manager开始做后续的消息接收逻辑
            manager.receiveMessage(tag)
    
# 根据消息的主循环，构造一个线程
# 启动主线程
# 返回的是一个线程
def startLoop(manager, stream) -> threading.Thread:
    thread = threading.Thread(
        target=messageLoop,
        args=(manager, stream)
    )
    # 启动这个线程
    thread.start()
    # 返回这个线程，方便上层管理
    return thread