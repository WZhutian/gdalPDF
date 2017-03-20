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

    def setPen(self,c="#FFFFFF",w="1px",\
        p="",penId="",cap="",j="",dp="",l=""):
        self.str = "PEN(c:" + c + ",w:" + w
        self.add(p,'p')
        self.add(penId,'id')
        self.add(cap,'cap')
        self.add(j,'j')
        self.add(dp,'dp')
        self.add(l,'l')
        self.str += ")"
        self.pen = self.str

    def setBrush(self,fc="#808080",bc="#808080",\
        brushId="",a="",s="",dx="",dy="",l=""):
        self.str = "BRUSH(fc:" + fc + ",bc:" + bc
        self.add(brushId,'id')
        self.add(a,'a')
        self.add(s,'s')
        self.add(dx,'dx')
        self.add(dy,'dy')
        self.add(l,'l')
        self.str += ")"
        self.brush = self.str

    def setSymbol(self,symbolId="",a="",c="#000000",\
        o="",s="",dx="",dy="",ds="",dp="",di="",l=""):
        self.str = "SYMBOL(c:" + c
        self.add(symbolId,'id')
        self.add(a,'a')
        self.add(o,'o')
        self.add(s,'s')
        self.add(dx,'dx')
        self.add(dy,'dy')
        self.add(ds,'ds')
        self.add(dp,'dp')
        self.add(di,'di')
        self.add(l,'l')
        self.str += ")"
        self.symbol = self.str

    def setLabel(self,f="",s="",t="",a="",c="#000000",\
        b="",o="",h="",w="",st="",m="",p="",dx="",dy="",dp="",bo="",it="",un="",l=""):
        self.str = "LABEL(c:" + c
        self.add(f,'f')
        self.add(s,'s')
        self.add(t,'t')
        self.add(a,'a')
        self.add(b,'b')
        self.add(o,'o')
        self.add(h,'h')
        self.add(w,'w')
        self.add(st,'st')
        self.add(m,'m')
        self.add(p,'p')
        self.add(dx,'dx')
        self.add(dy,'dy')
        self.add(dp,'dp')
        self.add(bo,'bo')
        self.add(it,'it')
        self.add(un,'un')
        self.add(l,'l')
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
    test = OgrFeatureStyle('line')
    test.setPen()
    print test.getSQL()
