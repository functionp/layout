class Test():
    def __init__(self):
        self.a = "soso"
        self.__pri()

    def __pri(self):
        self.a = "souhei"

s = Test()
print s.a
