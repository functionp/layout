
class Super():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Sub(Super):
    classval = "aaa"

    def __init__(self, x, y, z):
        Super.__init__(self,x,y)
        self.z = z


s1 = Sub(1,2,3)
s2 = Sub(1,2,3)
s3 = Sub(1,2,3)

l = [s1, s2, s3]

def function(l):
    l[0].x = l[1].y
    l[1].x = l[0].z

print l[0].x
print l[1].x

function(l)

print l[0].x
print l[1].x
