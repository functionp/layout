class TestA():
    def __init__(self, hoge):
        self.innerlayout = hoge

    @classmethod
    def classmethod1(cls, a):
        return TestA(a)

ins = TestA.classmethod1("soso")
print ins.innerlayout


