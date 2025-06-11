

# 这是给有分包需求的message准备的
# 有分包需求的信息可以把后续会用到的信息暂存在这里
class PackageMsgManager:
    def __init__(self):
        # 下一个要分配的info id
        self.nextId = 10000
        # 已经注册过的分包信息
        self.infoMap = {}
        # 远端信息
        self.remoteInfo = {}

    # 注册新的分包任务
    # packageInfo可能是各种数据类型，取决于message那边自己定义
    def registerPackageTask(self,packageInfo):
        self.infoMap[self.nextId] = packageInfo
        self.nextId = self.nextId + 1
        return self.nextId - 1

    # 注册远端信息的任务
    # 它的特殊性在于需要把infoId也由外部传进来
    def registerRemotePackage(self,infoId, packageInfo):
        self.remoteInfo[infoId] = packageInfo

    # 删除分包任务
    def deletePackageInfo(self,infoId):
        self.infoMap.pop(infoId)

    # 删除远端任务
    def deleteRemotePackage(self,infoId):
        self.remoteInfo.pop(infoId)

    # 获取本地的package
    def getLocalPackage(self,infoId):
        if infoId not in self.infoMap:
            raise RuntimeError(f'Cannot find {infoId} in local package.')
        return self.infoMap[infoId]

    # 获取远程的package
    def getRemotePackage(self,infoId):
        if infoId not in self.remoteInfo:
            raise RuntimeError(f'Cannot find {infoId} in remote package.')
        return self.remoteInfo[infoId]