# -*- coding: utf-8 -*-


class Node:
    def __init__(self, op, children=[]):
        self.op = op
        self.children = children
    
    #木構造を表示するインスタンスメソッド
    def display(self, depth):
        
        tabs = "  " * depth

        for child in self.children:
            
            #節点か末端か
            if isinstance(child, Node):
                print tabs + child.op
                child.display(depth + 1)
            else:

                #オブジェクト構造体か否か
                if isinstance(child, Obst):

                    #相対番地が必要な場合＝深さ0以外のPARAMかVAR、かつ初めの宣言
                    if (child.kind == 'PARAM' or child.kind == 'VAR') and child.lev > 0 and child.offset != None:
                        print tabs +"(%s,%s,%d,%d) " % (child.name, child.kind, child.lev, child.offset)
                    elif child.kind == 'FUN':
                        print tabs +"(%s,%s,arg:%d,top:%d)" % (child.name, child.kind, child.argnum,child.top_alloc)
                    else:
                        print tabs +"(%s,%s,%d) " % (child.name, child.kind, child.lev)
                else:
                    print tabs + str(child)
        
