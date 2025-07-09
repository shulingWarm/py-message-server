from AbstractMessage import AbstractMessage

class ArrayFinishMessage(AbstractMessage):
    def __init__(self, name):
        super().__init__(name)

    def setIdArrayPackage(self, idArrayPackage):
        self.idArrayPackage = idArrayPackage