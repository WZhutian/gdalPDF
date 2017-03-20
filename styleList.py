# -*- coding:utf-8 -*-
class OgrFeatureStyle(object):
    def __init__(self,type):
        self.type = type
        self.str = ""
        self.pen = ""
        self.brush = ""
        self.symbol = ""
        self.label = ""

    def add(self,value,typeName):
        if value:
            self.str += "," + typeName + ":\"" + value + "\""

    '''
    c="#FFFFFF",w="1px",p="",penId="",cap="",j="",dp="",l=""
    '''
    def setPen(self,c="#FFFFFF",w="1px",**kwargs):
        self.str = "PEN(c:" + c + ",w:" + w
        for key in kwargs:
            self.add(kwargs[key],key)
        self.str += ")"
        self.pen = self.str
    '''
        fc="#808080",bc="#808080",brushId="",a="",s="",dx="",dy="",l=""
    '''
    def setBrush(self,fc="#808080",bc="#808080",**kwargs):
        self.str = "BRUSH(fc:" + fc + ",bc:" + bc
        for key in kwargs:
            self.add(kwargs[key],key)
        self.str += ")"
        self.brush = self.str

    '''
        symbolId="",a="",c="#000000",o="",s="",dx="",dy="",ds="",dp="",di="",l=""
    '''
    def setSymbol(self,c="#000000",**kwargs):
        self.str = "SYMBOL(c:" + c
        for key in kwargs:
            self.add(kwargs[key],key)
        self.str += ")"
        self.symbol = self.str

    '''
        f="",s="",t="",a="",c="#000000",b="",o="",h="",w="",st="",m="",p="",
        dx="",dy="",dp="",bo="",it="",un="",l=""
    '''
    def setLabel(self,c="#000000",**kwargs):
        self.str = "LABEL(c:" + c
        for key in kwargs:
            self.add(kwargs[key],key)
        self.str += ")"
        self.label = self.str

    def getSQL(self):
        if self.type == "point":
            return self.symbol
        elif self.type == "line":
            return self.pen
        elif self.type == "polygon":
            return self.pen + ";" + self.brush
        elif self.type == "label":
            return self.label
#执行测试区域
if __name__=='__main__':
    test = OgrFeatureStyle('polygon')
    test.setBrush("#d70000","#d70000")
    test.setPen("#1382e9")
    print test.getSQL()
