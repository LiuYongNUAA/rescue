# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import Configure
from GraphicsView import *
from GraphicsLineItem import *
import sys
import UI_mainwindow
import math
from math import sin, cos
import planeposition
from SinglePoint import *
from configobj import ConfigObj

PI = math.pi

class Mainwindow(QMainWindow, UI_mainwindow.Ui_WaterRescue):
    def __init__(self, parent=None):
        super(Mainwindow, self).__init__(parent)
        self.setupUi(self)

        self.graphicsView = GraphicsView()
        self.verticalLayout_5.addWidget(self.graphicsView)
        self.graphicsView.setGeometry(0, 0, 874, 600)
        self.viewwidth = self.graphicsView.width()
        self.viewheight = self.graphicsView.height()
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(-self.viewwidth * 100, -self.viewheight * 100, self.viewwidth * 200,
                                self.viewheight * 200)
        # 这样就不会被大小限制住，这样scene可以随着view的变化而变化。
        self.graphicsView.setScene(self.scene)
        self.deleteitemsx = []
        self.deleteitemsy = []
        self.circleitem = []
        self.axisitemx = []
        self.axisitemy = []
        self.textitemx = []
        self.textitemy = []
        self.sc = 1
        self.lastsc = 1
        self.sumscale = 1
        self.jishu = 1
        self.start = 0
        self.fenmiao = 1
        self.NS = 'N'
        self.WE = 'E'
        self.addorigin = False
        self.xiugaihouzuobiao = None
        self.origin = None
        self.listpositionexample = None
        self.addpositionexample = None
        self.updateUi()


        self.connect(self.filedefault, SIGNAL('triggered()'), self.configure)

    def xfloat(self, DWL, CWL, SeaSp, SeaA, TrendSp, TrenA, WcS, WcA, WindA):
        return DWL * sin(WindA) + CWL * cos(WindA) + SeaSp * sin(SeaA) + TrendSp * sin(TrenA) + WcS * sin(WcA)

    def yfloat(self,DWL, CWL, SeaSp, SeaA, TrendSp, TrenA, WcS, WcA, WindA):
        return DWL * cos(WindA) - CWL * sin(WindA) + SeaSp * cos(SeaA) + TrendSp * cos(TrenA) + WcS * cos(WcA)

    def Float(self):
        conf = ConfigObj('Config')
        MenDWL = float(conf['MenDWL'])/ 100
        MenCWL = float(conf['MenCWL']) / 100
        MenDWLerror = float(conf['MenDWLerror']) / 100
        MenCWLerror = float(conf['MenCWLerror']) / 100
        LifeBoatDWL = float(conf['LifeBoatDWL']) / 100
        LifeBoatCWL = float(conf['LifeBoatCWL']) / 100
        LifeBoatDWLerror = float(conf['LifeBoatDWLerror']) /100
        LifeBoatCWLerror = float(conf['LifeBoatCWLerror']) /100
        ShipDWL = float(conf['ShipDWL']) / 100
        ShipCWL = float(conf['ShipCWL']) / 100
        ShipDWLerror = float(conf['ShipDWLerror']) / 100
        ShipCWLerror = float(conf['ShipCWLerror']) / 100
        WindSpeed = self.WindSpeeddoubleSpinBox.value() / 3.6
        WindAngle = self.WindAngledoubleSpinBox.value() * PI / 180
        SeaSpeed = self.SeaSpeeddoubleSpinBox.value() / 3.6
        SeaAngle = self.SeaAngledoubleSpinBox.value() * PI / 180
        TrendSpeed = self.TrendSpeeddoubleSpinBox.value() / 3.6
        TrendAngle = self.TrendAngledoubleSpinBox.value() * PI / 180
        Time = self.TimespinBox_1.value()*3600 + self.TimespinBox_2.value()*60 + self.TimespinBox_3.value()
        MenDWLSpeed = MenDWL * WindSpeed + MenDWLerror
        MenCWLSpeed = MenCWL * WindSpeed + MenCWLerror
        LifeDWLSpeed = LifeBoatDWL * WindSpeed + LifeBoatDWLerror
        LifeCWLSpeed = LifeBoatCWL * WindSpeed + LifeBoatCWLerror
        ShipDWLSpeed = ShipDWL * WindSpeed + ShipDWLerror
        ShipCWLSpeed = ShipCWL * WindSpeed + ShipCWLerror
        if WindSpeed < 9.25:
            Wc_Speed = 0.09
        else:
            Wc_Speed = (0.230446 + 0.0070957 * WindSpeed * 0.514) ** 2 + 0.09
        Wc_Angle = (-35.338 + 3587.98 / (0.514 * WindSpeed) + WindAngle) * PI / 180
        Menxfloat = self.xfloat(MenDWLSpeed, MenCWLSpeed, SeaSpeed, SeaAngle, TrendSpeed, TrendAngle, Wc_Speed, Wc_Angle, WindAngle) * Time
        Menyfloat = self.yfloat(MenDWLSpeed, MenCWLSpeed, SeaSpeed, SeaAngle, TrendSpeed, TrendAngle, Wc_Speed, Wc_Angle, WindAngle) * Time
        Lifexfloat = self.xfloat(LifeDWLSpeed, LifeCWLSpeed, SeaSpeed, SeaAngle, TrendSpeed, TrendAngle, Wc_Speed, Wc_Angle, WindAngle) * Time
        Lifeyfloat = self.yfloat(LifeDWLSpeed, LifeCWLSpeed, SeaSpeed, SeaAngle, TrendSpeed, TrendAngle, Wc_Speed, Wc_Angle, WindAngle) * Time
        Shipxfloat = self.xfloat(ShipDWLSpeed, ShipCWLSpeed, SeaSpeed, SeaAngle, TrendSpeed, TrendAngle, Wc_Speed, Wc_Angle, WindAngle) * Time
        Shipyfloat = self.yfloat(ShipDWLSpeed, ShipCWLSpeed, SeaSpeed, SeaAngle, TrendSpeed, TrendAngle, Wc_Speed, Wc_Angle, WindAngle) * Time

    def p(self,s=None):
        if not s:
            return
        self.__dirty=True
        self.start = 0
        self.addorigin=True
        if self.circleitem:
            self.graphicsView.scale(1 / self.sumscale,
                                    1 / self.sumscale)
            for i in self.circleitem:
                if i.pos().x()>= -self.viewwidth * 100 and i.pos().x() <= self.viewwidth * 100\
                        and i.pos().y()>= -self.viewheight * 100 and i.pos().y() <= self.viewheight * 100:
                    self.scene.removeItem(i)
            self.circleitem=[]
            self.graphicsView.centerOn(QPoint(0,0))
            self.sumscale = 1
        weidu, jingdu=s.split('-')
        self.originj = jingdu.split(',')
        self.originw = weidu.split(',')
        self.NS=weidu[-1]
        self.WE=jingdu[-1]
        self.xiugaihouzuobiao = self.initialize()
        linshi=self.pointpos([self.originw, self.originj])
        self.updateUi()
        self.axis()

    def initialize(self):
        self.__dirty=True
        choice=[]
        for i in range(61):
            choice.append(int(i))
        a=self.originw
        b=self.originj
        c=[]
        if self.NS=='N':
            for i in choice:
                if i>=float(a[2][:-1]):
                    break
        elif self.NS=='S':
            for i in choice:
                if i>=float(a[2][:-1]):
                    if i!=0:
                        i-=10
                    break
        if i!=60:
            c.append([a[0], a[1], i])
        else:
            if int(a[1])+1==60:
                c.append([int(a[0])+1, 0, 0])
            else:
                c.append([a[0], int(a[1])+1, 0])
        if self.WE=='E':
            for i in choice:
                if i>=float(b[2][:-1]):
                    break
        elif self.WE=='W':
            for i in choice:
                if i>=float(b[2][:-1]):
                    if i!=0:
                        i-=10
                    break
        if i!=60:
            c.append([b[0], b[1], i])
        else:
            if int(a[1])+1==60:
                c.append([int(b[0])+1, 0, 0])
            else:
                c.append([b[0], int(b[1])+1, 0])
        return c
    def convert1(self, index, NSWE=None):
        self.__dirty=True
        if self.NS=='N' or NSWE=='N':
            index=-index/100
        else:
            index=index/100
        if index>=0:
            a = self.xiugaihouzuobiao[0][2]+index % 60
            b = int(self.xiugaihouzuobiao[0][1])+int(index / 60) % 60
            c = int(self.xiugaihouzuobiao[0][0])+int(index / 60 / 60)
        else:
            a = self.xiugaihouzuobiao[0][2]-abs(index) % 60
            b = int(self.xiugaihouzuobiao[0][1])-int(abs(index) / 60) % 60
            c = int(self.xiugaihouzuobiao[0][0])-int(abs(index) / 60 / 60)
        if a>=60:
            a-=60
            b+=1
        elif a<0:
            a+=60
            b-=1
        if b>=60:
            b-=60
            c+=1
        elif b<0:
            b+=60
            c-=1
        if c==b==a==0:
            return "0°0'0''"
        if c>=0 and  self.NS=='N':
            return "%s°%s'%.5s''N" % (c, b, a)
        elif c<0 and self.NS=='N':
            if a==0:
                a=0
                if b==0:
                    b=0
                    c=-c
                else:
                    b=60-b
                    c=-c-1
            else:
                a=60-a
                b=60-b-1
                c=-c-1
            return "%s°%s'%.5s''S" % (c, b, a)
        if c>=0 and  self.NS=='S':
            return "%s°%s'%.5s''S" % (c, b, a)
        elif c<0 and self.NS=='S':
            if a==0:
                a=0
                if b==0:
                    b=0
                    c=-c
                else:
                    b=60-b
                    c=-c-1
            else:
                a=60-a
                b=60-b-1
                c=-c-1
            return "%s°%s'%.5s''N" % (c, b, a)

    def convert2(self, index, NSWE=None):
        self.__dirty=True
        if self.NS=='N' or NSWE=='N':
            index=-index/100
            c = index / 60 / 60+int(self.xiugaihouzuobiao[0][0])\
                +int(self.xiugaihouzuobiao[0][1])/60+self.xiugaihouzuobiao[0][2]/3600
            if c==0:
                return "0°"
            elif c>0:
                return "%.7s°N" % (c)
            elif c<0:
                return "%.7s°S" % (-c)
        else:
            index=index/100
            c = index / 60 / 60+int(self.xiugaihouzuobiao[0][0])\
                +int(self.xiugaihouzuobiao[0][1])/60+self.xiugaihouzuobiao[0][2]/3600
            if c==0:
                return "0°"
            elif c>0:
                return "%.7s°S" % (c)
            elif c<0:
                return "%.7s°N" % (-c)

    def convert3(self, index, NSWE=None):
        self.__dirty=True
        if self.WE=='E' or NSWE=='E':
            index=-index/100
        else:
            index=index/100
        if index>=0:
                a = self.xiugaihouzuobiao[1][2]-index % 60
                b = int(self.xiugaihouzuobiao[1][1])-int(index / 60) % 60
                c = int(self.xiugaihouzuobiao[1][0])-int(index / 60 / 60)
        else:
                a = self.xiugaihouzuobiao[1][2]+abs(index) % 60
                b = int(self.xiugaihouzuobiao[1][1])+int(abs(index) / 60) % 60
                c = int(self.xiugaihouzuobiao[1][0])+int(abs(index) / 60 / 60)
        if a >= 60:
                a -= 60
                b += 1
        elif a < 0:
                a += 60
                b -= 1
        if b >= 60:
                b -= 60
                c += 1
        elif b < 0:
                b += 60
                c -= 1
        if c==b==a==0:
            return "0°0'0''"

        if c>=0 and  self.WE=='E':
            if c<180:
                return "%s°%s'%.5s''E" % (c, b, a)
            elif c==180 :
                if b==a==0:
                    return "180°0'0''"
                elif a==0:
                    return "%s°%s'%.5s''W" % (179, 60-b, 0)
                else:
                    return "%s°%s'%.5s''W" % (179, 59-b, 60-a)
            elif c>180:
                if a==0:
                    a=0
                    if b==0:
                        c=360-c
                    else:
                        b=60-b
                        c=359-c
                else:
                    a=60-a
                    b=59-b
                    c=359-c
                return "%s°%s'%.5s''W" % (c, b, a)

        elif c<0 and self.WE=='E':
            if a==0:
                a=0
                if b==0:
                    b=0
                    c=-c
                else:
                    b=60-b
                    c=-c-1
            else:
                a=60-a
                b=60-b-1
                c=-c-1
            if c<180:
                return "%s°%s'%.5s''W" % (c, b, a)
            if c==180 and b==a==0:
                return "180°0'0''"
            if c>180:
                if a==0:
                    a=0
                    if b==0:
                        c=360-c
                    else:
                        b=60-b
                        c=359-c
                else:
                    a=60-a
                    b=59-b
                    c=359-c
                return "%s°%s'%.5s''E" % (c, b, a)

        if c>=0 and  self.WE=='W':
            if c<180:
                return "%s°%s'%.5s''W" % (c, b, a)
            elif c==180 :
                if b==a==0:
                    return "180°0'0''"
                elif a==0:
                    return "%s°%s'%.5s''E" % (179, 60-b, 0)
                else:
                    return "%s°%s'%.5s''E" % (179, 59-b, 60-a)
            elif c>180:
                if a==0:
                    a=0
                    if b==0:
                        c=360-c
                    else:
                        b=60-b
                        c=359-c
                else:
                    a=60-a
                    b=59-b
                    c=359-c
                return "%s°%s'%.5s''E" % (c, b, a)

        elif c<0 and self.WE=='W':
            if a==0:
                a=0
                if b==0:
                    b=0
                    c=-c
                else:
                    b=60-b
                    c=-c-1
            else:
                a=60-a
                b=60-b-1
                c=-c-1
            if c<180:
                return "%s°%s'%.5s''E" % (c, b, a)
            if c==180 and b==a==0:
                return "180°0'0''"
            if c>180:
                if a==0:
                    a=0
                    if b==0:
                        c=360-c
                    else:
                        b=60-b
                        c=359-c
                else:
                    a=60-a
                    b=59-b
                    c=359-c
                return "%s°%s'%.5s''W" % (c, b, a)


    def convert4(self, index, NSWE=None):
        self.__dirty=True
        if self.WE=='E' or NSWE=='E':
            index=-index/100
            c = index / 60 / 60+int(self.xiugaihouzuobiao[0][0])\
                +int(self.xiugaihouzuobiao[0][1])/60+self.xiugaihouzuobiao[0][2]/3600
            if c==0:
                return "0°"
            elif c>0:
                return "%.7s°W" % (c)
            elif c==180:
                return "180°"
            elif c>180:
                return "%.7s°E" % (360-c)
            elif c<0:
                return "%.7s°E" % (-c)
        else:
            index=index/100
            c = index / 60 / 60+int(self.xiugaihouzuobiao[0][0])\
                +int(self.xiugaihouzuobiao[0][1])/60+self.xiugaihouzuobiao[0][2]/3600
            if c==0:
                return "0°"
            elif c>0 and c<180:
                return "%.7s°E" % (c)
            elif c==180:
                return "180°"
            elif c>180:
                return "%.7s°W" % (360-c)
            elif c<0:
                return "%.7s°W" % (-c)


    def axis(self):
        self.__dirty=True
        pos1 = self.graphicsView.mapToScene(0, 0)
        pos2 = self.graphicsView.mapToScene(self.graphicsView.width(), self.graphicsView.height())
        for i in self.textitemx:
            self.scene.removeItem(i)
        self.textitemx = []
        for i in self.textitemy:
            self.scene.removeItem(i)
        self.textitemy = []
        pos3 = [(-pos1.x() + pos2.x()) / 15+pos1.x(), (pos1.y() - pos2.y()) / 10+pos2.y()]
        for i in self.axisitemx:
            if i.index >= -self.viewwidth * 100 and i.index <= self.viewwidth * 100:
                h = QGraphicsTextItem()
                h.setPlainText('%s' % str(self.convert3(i.index)) if self.fenmiao==1\
                        else '%s'%str(self.convert4(i.index)))
                self.textitemx.append(h)
                h.setPos(i.index, pos3[1])
                self.scene.addItem(h)
                h.setScale(1 / self.sumscale)
        for i in self.axisitemy:
            if i.index >= -self.viewheight * 100 and i.index <= self.viewheight * 100:
                h = QGraphicsTextItem()
                h.setPlainText('%s' % str(self.convert1(i.index)) if self.fenmiao==1\
                        else '%s' %str(self.convert2(i.index)))
                self.textitemy.append(h)
                h.setPos(pos3[0], i.index)
                h.rotate(90)
                self.scene.addItem(h)
                h.setScale(1/ self.sumscale)

    def pointzuobiao(self, pos):
        self.__dirty=True
        pointx=self.convert1(pos.y())
        pointy=self.convert3(pos.x())

        return('%s,%s'%(pointx, pointy))


    def pointpos1(self, zuobiao=None):#坐标形式为["0°0'0''N", "0°0'0''E"]
        a = zuobiao[0].split('°')
        du = a[0]
        b = a[1].split("'")
        fen = b[0]
        miao = b[1]+b[3]
        a = zuobiao[1].split('°')
        du1 = a[0]
        b = a[1].split("'")
        fen1 = b[0]
        miao1 = b[1]+b[3]

        print([du + fen/60 + miao/360,du1 + fen1/60 +miao1/360 ])
        return([[du,fen,miao], [du1,fen1,miao1]])


    def pointpos(self, zuobiao=None):#坐标形式为（[[0,0,000N],[0,0,00E]]）
        self.__dirty=True
        if zuobiao and self.xiugaihouzuobiao:
            a=int(self.xiugaihouzuobiao[0][0])*3600 \
            + int(self.xiugaihouzuobiao[0][1]) * 60 + self.xiugaihouzuobiao[0][2]
            if zuobiao[0][2][-1]=='N' or zuobiao[0][2][-1]=='S':
                b=int(zuobiao[0][0])*3600 \
                + int(zuobiao[0][1]) * 60 + float(zuobiao[0][2][:-1])
            else:
                b = int(zuobiao[0][0]) * 3600 \
                    + int(zuobiao[0][1]) * 60 + float(zuobiao[0][2])
            c=int(self.xiugaihouzuobiao[1][0]) *3600\
            + int(self.xiugaihouzuobiao[1][1]) * 60 + self.xiugaihouzuobiao[1][2]
            if zuobiao[1][2][-1]=="E" or zuobiao[1][2][-1]=='W':
                d=int(zuobiao[1][0])*3600 \
                + int(zuobiao[1][1]) * 60 + float(zuobiao[1][2][:-1])
            else:
                d = int(zuobiao[1][0]) * 3600 \
                    + int(zuobiao[1][1]) * 60 + float(zuobiao[1][2])

            if a==0:
                if zuobiao[0][2][-1]=='N':
                    e=a-b
                elif zuobiao[0][2][-1]=='S':
                    e=b-a
                else:
                    e=0
            elif a!=0:
                if self.NS=='N':
                    if zuobiao[0][2][-1]=='N':
                        e=a-b
                    elif zuobiao[0][2][-1]=='S':
                        e=a+b
                    else:
                        e=a
                elif self.NS=='S':
                    if zuobiao[0][2][-1]=='N':
                        e=-a-b
                    elif zuobiao[0][2][-1]=='S':
                        e=b-a
                    else:
                        e=-a
            if b==0:
                if zuobiao[1][2][-1]=='W':
                    f=c-d
                elif zuobiao[1][2][-1]=='E':
                    f=d-c
                else:
                    f=0
            elif b!=0:
                if self.WE=='E':
                    if zuobiao[1][2][-1]=='E':
                        f=d-c
                    elif zuobiao[1][2][-1]=='W':
                        f=-d-c
                    else:
                        f=-c
                elif self.WE=='W':
                    if zuobiao[1][2][-1]=='W':
                        f=c-d
                    elif zuobiao[1][2][-1]=='E':
                        f=d+c
                    else:
                        f=c
            return QPoint(100*f,100*e)


    def updateUi(self, Pos=None):
        self.__dirty=True
        if self.sumscale == 1 and self.start==0:
            for i in self.axisitemx:
                if i.index >= -self.viewwidth * 100 and i.index <= self.viewwidth * 100:
                    self.scene.removeItem(i)
                del i
            self.axisitemx = []
            for i in self.axisitemy:
                if i.index >= -self.viewheight * 100 and i.index <= self.viewheight * 100:
                    self.scene.removeItem(i)
                del i
            self.axisitemy = []
            n=1
            jishu=-15 * 200
            while n<=31:
                linshi = GraphicsLineItem(jishu, -self.viewheight * 100, jishu, self.viewheight * 100)
                linshi .setindex(jishu)
                linshi.setPen(QPen(QColor(10, 100, 240)))
                self.axisitemx.append(linshi)
                self.scene.addItem(linshi)
                n+=1
                jishu+=200

            jishu = -15 * 200
            n=1
            while n<=31:
                linshi = GraphicsLineItem(-self.viewwidth * 100, jishu, self.viewwidth * 100, jishu)
                linshi .setindex(jishu)
                linshi.setPen(QPen(QColor(10, 100, 240)))
                self.axisitemy.append(linshi)
                self.scene.addItem(linshi)
                jishu += 200
                n+=1



        elif self.lastsc >= 2:
            for i in self.axisitemx:
                if i.index >= -self.viewwidth * 100 and i.index <= self.viewwidth * 100:
                    self.scene.removeItem(i)
            for i in range(len(self.axisitemx)):
                self.deleteitemsx.append(i)
            self.deleteitemsx.reverse()
            self.deleteitemsx.pop()
            span = (self.axisitemx[1].index - self.axisitemx[0].index) / 2
            for i in self.deleteitemsx:
                linshi = GraphicsLineItem(self.axisitemx[i].index - span, -self.viewheight * 100,
                                           self.axisitemx[i].index - span, self.viewheight * 100)
                linshi.setPen(QPen(QColor(10, 100, 240)))
                linshi.setindex(self.axisitemx[i].index - span)
                self.axisitemx.insert(i, linshi)
            n=len(self.axisitemx)
            for i in range(int(n/4)):
                self.axisitemx.pop(len(self.axisitemx)-1)
                self.axisitemx.pop(0)
            self.deleteitemsx = []
            for i in self.axisitemx:
                if i.index >= -self.viewwidth * 100 and i.index <= self.viewwidth * 100:
                    self.scene.addItem(i)

            for i in self.axisitemy:
                if i.index >= -self.viewheight * 100 and i.index <= self.viewheight * 100:
                    self.scene.removeItem(i)
            for i in range(len(self.axisitemy)):
                self.deleteitemsy.append(i)
            self.deleteitemsy.reverse()
            self.deleteitemsy.pop()
            span = (self.axisitemy[1].index - self.axisitemy[0].index) / 2
            for i in self.deleteitemsy:
                linshi = GraphicsLineItem(-self.viewwidth * 100, self.axisitemy[i].index - span,
                                           self.viewwidth * 100, self.axisitemy[i].index - span)
                linshi.setPen(QPen(QColor(10, 100, 240)))
                linshi .setindex( self.axisitemy[i].index - span)
                self.axisitemy.insert(i, linshi)
            n=len(self.axisitemy)
            for i in range(int(n/4)):
                self.axisitemy.pop(len(self.axisitemy)-1)
                self.axisitemy.pop(0)
            self.deleteitemsy = []
            for i in self.axisitemy:
                if i.index >= -self.viewheight * 100 and i.index <= self.viewheight * 100:
                    self.scene.addItem(i)
            for i in range(len(self.axisitemx)):
                if self.axisitemx[i].index>Pos.x():
                    break
            n= int(i-(len(self.axisitemx)-1)/2)
            span=self.axisitemx[1].index-self.axisitemx[0].index
            if n>0:
                for i in range(n):
                    linshi=GraphicsLineItem(self.axisitemx[len(self.axisitemx) - 1].index + span,
                                            -self.viewheight * 100,
                                            self.axisitemx[len(self.axisitemx) - 1].index + span,
                                            self.viewheight * 100)
                    linshi.setPen(QPen(QColor(10,100,240)))
                    linshi.setindex(self.axisitemx[len(self.axisitemx) - 1].index + span)
                    if self.axisitemx[0].index >= -self.viewwidth * 100 \
                            and self.axisitemx[0].index <= self.viewwidth * 100:
                        self.scene.removeItem(self.axisitemx[0])
                    if linshi.index <= self.viewwidth * 100 and linshi.index>= -100 * self.viewwidth:
                        self.scene.addItem(linshi)
                    self.axisitemx.append(linshi)
                    self.axisitemx.pop(0)
            elif n<0:
                for i in range(-n):
                    linshi=GraphicsLineItem(self.axisitemx[0].index - span, -self.viewheight * 100,
                                            self.axisitemx[0].index - span, self.viewheight * 100)
                    linshi.setPen(QPen(QColor(10,100,240)))
                    linshi.setindex(self.axisitemx[0].index - span)
                    if self.axisitemx[len(self.axisitemx) - 1].index >= -self.viewwidth * 100 \
                            and self.axisitemx[len(self.axisitemx) - 1].index <= self.viewwidth * 100:
                        self.scene.removeItem(self.axisitemx[len(self.axisitemx) - 1])
                    if linshi.index <= self.viewwidth * 100 and linshi.index>= -self.viewwidth*100:
                        self.scene.addItem(linshi)
                    self.axisitemx.insert(0, linshi)
                    self.axisitemx.pop()



            for i in range(len(self.axisitemy)):
                 if self.axisitemy[i].index > Pos.y():
                     break
            n = int(i - (len(self.axisitemx) - 1) / 2)
            span=self.axisitemy[1].index-self.axisitemy[0].index
            if n>0:
                for i in range(n):
                    linshi = GraphicsLineItem(-self.viewwidth * 100, self.axisitemy[len(self.axisitemy) - 1].index + span,
                                              self.viewwidth * 100, self.axisitemy[len(self.axisitemy) - 1].index + span)
                    linshi.setPen(QPen(QColor(10, 100, 240)))
                    linshi.setindex(self.axisitemy[len(self.axisitemy) - 1].index + span)
                    if self.axisitemy[0].index <= self.viewheight * 100 and self.axisitemy[
                        0].index >= -self.viewheight * 100:
                        self.scene.removeItem(self.axisitemy[0])
                    if linshi.index <= self.viewheight * 100 and linshi.index>= -self.viewheight*100:
                        self.scene.addItem(linshi)
                    self.axisitemy.append(linshi)
                    self.axisitemy.pop(0)
            elif n<0:
                for i in range(-n):
                    linshi = GraphicsLineItem(-self.viewwidth * 100,
                                              self.axisitemy[0].index - span,
                                              self.viewwidth * 100,
                                              self.axisitemy[0].index - span)
                    linshi.setPen(QPen(QColor(10, 100, 240)))
                    linshi.setindex(self.axisitemy[0].index - span)
                    if self.axisitemy[len(self.axisitemy) - 1].index >= -self.viewheight * 100 \
                            and self.axisitemy[len(self.axisitemy) - 1].index <= self.viewheight * 100:
                        self.scene.removeItem(self.axisitemy[len(self.axisitemy) - 1])
                    if linshi.index <= self.viewheight * 100 and linshi.index >= -self.viewheight * 100:
                        self.scene.addItem(linshi)
                    self.axisitemy.insert(0, linshi)
                    self.axisitemy.pop()






        elif self.lastsc <=0.5:
            span=self.axisitemx[1].index-self.axisitemx[0].index
            n=len(self.axisitemx)
            for i in range(int(n/2)):
                linshi = GraphicsLineItem(self.axisitemx[0].index - span, -self.viewheight * 100,
                                           self.axisitemx[0].index - span, self.viewheight * 100)
                linshi.setPen(QPen(QColor(10, 100, 240)))
                linshi.setindex(self.axisitemx[0].index - span)
                self.axisitemx.insert(0, linshi)
                if linshi.index >= -self.viewwidth * 100 and linshi.index <= self.viewwidth * 100:
                    self.scene.addItem(linshi)
                linshi=GraphicsLineItem(self.axisitemx[len(self.axisitemx)-1].index + span, -self.viewheight * 100,
                                           self.axisitemx[len(self.axisitemx)-1].index + span, self.viewheight * 100)
                linshi.setPen(QPen(QColor(10,100,240)))
                linshi.setindex(self.axisitemx[len(self.axisitemx)-1].index + span)
                self.axisitemx.append(linshi)
                if linshi.index >= -self.viewwidth * 100 and linshi.index <= self.viewwidth * 100:
                    self.scene.addItem(linshi)
            for i in range(len(self.axisitemx)):
                if i % 2 != 0:
                    self.deleteitemsx.append(i)
            self.deleteitemsx.reverse()
            for i in self.deleteitemsx:
                if self.axisitemx[i].index>=-self.viewwidth*100 and self.axisitemx[i].index<=self.viewwidth*100:
                    self.scene.removeItem(self.axisitemx[i])
                self.axisitemx.pop(i)
            self.deleteitemsx = []


            span = self.axisitemy[1].index - self.axisitemy[0].index
            n = len(self.axisitemy)
            for i in range(int(n / 2)):
                linshi = GraphicsLineItem( -self.viewwidth * 100,self.axisitemy[0].index - span,
                                           self.viewwidth * 100, self.axisitemy[0].index - span)
                linshi.setPen(QPen(QColor(10, 100, 240)))
                linshi.setindex(self.axisitemy[0].index - span)
                self.axisitemy.insert(0, linshi)
                if linshi.index >= -self.viewheight * 100 and linshi.index <= self.viewheight * 100:
                    self.scene.addItem(linshi)
                linshi = GraphicsLineItem(-self.viewwidth * 100, self.axisitemy[len(self.axisitemy) - 1].index + span,
                                           self.viewwidth * 100, self.axisitemy[len(self.axisitemy) - 1].index + span)
                linshi.setPen(QPen(QColor(10, 100, 240)))
                linshi.setindex(self.axisitemy[len(self.axisitemy) - 1].index + span)
                self.axisitemy.append(linshi)
                if linshi.index >= -self.viewheight * 100 and linshi.index <= self.viewheight * 100:
                    self.scene.addItem(linshi)
            for i in range(len(self.axisitemy)):
                if i % 2 != 0:
                    self.deleteitemsy.append(i)
            self.deleteitemsy.reverse()
            for i in self.deleteitemsy:
                if self.axisitemy[i].index <= self.viewheight * 100 and self.axisitemy[
                    i].index >= -self.viewheight * 100:
                    self.scene.removeItem(self.axisitemy[i])
                self.axisitemy.pop(i)
            self.deleteitemsy = []

            for i in range(len(self.axisitemx)):
                if self.axisitemx[i].index>Pos.x():
                    break
            n= int(i-(len(self.axisitemx)-1)/2)
            span=self.axisitemx[1].index-self.axisitemx[0].index
            if n>0:
                for i in range(n):
                    linshi=GraphicsLineItem(self.axisitemx[len(self.axisitemx) - 1].index + span, -self.viewheight * 100,
                                            self.axisitemx[len(self.axisitemx) - 1].index + span, self.viewheight * 100)
                    linshi.setPen(QPen(QColor(10,100,240)))
                    linshi.setindex(self.axisitemx[len(self.axisitemx) - 1].index + span)
                    if self.axisitemx[0].index >= -self.viewwidth * 100 and self.axisitemx[0].index <= self.viewwidth * 100:
                        self.scene.removeItem(self.axisitemx[0])
                    if linshi.index <= self.viewwidth * 100 and linshi.index>= -100 * self.viewwidth:
                        self.scene.addItem(linshi)
                    self.axisitemx.append(linshi)
                    self.axisitemx.pop(0)
            elif n<0:
                for i in range(-n):
                    linshi=GraphicsLineItem(self.axisitemx[0].index - span, -self.viewheight * 100,
                                            self.axisitemx[0].index - span, self.viewheight * 100)
                    linshi.setPen(QPen(QColor(10,100,240)))
                    linshi.setindex(self.axisitemx[0].index - span)
                    if self.axisitemx[len(self.axisitemx) - 1].index >= -self.viewwidth * 100 \
                            and self.axisitemx[len(self.axisitemx) - 1].index <= self.viewwidth * 100:
                        self.scene.removeItem(self.axisitemx[len(self.axisitemx) - 1])
                    if linshi.index <= self.viewwidth * 100 and linshi.index>= -self.viewwidth*100:
                        self.scene.addItem(linshi)
                    self.axisitemx.insert(0, linshi)
                    self.axisitemx.pop()



            for i in range(len(self.axisitemy)):
                 if self.axisitemy[i].index > Pos.y():
                     break
            n = int(i - (len(self.axisitemx) - 1) / 2)
            span=self.axisitemy[1].index-self.axisitemy[0].index
            if n>0:
                for i in range(n):
                    linshi = GraphicsLineItem(-self.viewwidth * 100, self.axisitemy[len(self.axisitemy) - 1].index + span,
                                              self.viewwidth * 100, self.axisitemy[len(self.axisitemy) - 1].index + span)
                    linshi.setPen(QPen(QColor(10, 100, 240)))
                    linshi.setindex(self.axisitemy[len(self.axisitemy) - 1].index + span)
                    if self.axisitemy[0].index <= self.viewheight * 100 and self.axisitemy[
                        0].index >= -self.viewheight * 100:
                        self.scene.removeItem(self.axisitemy[0])
                    if linshi.index <= self.viewheight * 100 and linshi.index>= -self.viewheight*100:
                        self.scene.addItem(linshi)
                    self.axisitemy.append(linshi)
                    self.axisitemy.pop(0)
            elif n<0:
                for i in range(-n):
                    linshi = GraphicsLineItem(-self.viewwidth * 100,
                                              self.axisitemy[0].index - span,
                                              self.viewwidth * 100,
                                              self.axisitemy[0].index - span)
                    linshi.setPen(QPen(QColor(10, 100, 240)))
                    linshi.setindex(self.axisitemy[0].index - span)
                    if self.axisitemy[len(self.axisitemy) - 1].index >= -self.viewheight * 100 \
                            and self.axisitemy[len(self.axisitemy) - 1].index <= self.viewheight * 100:
                        self.scene.removeItem(self.axisitemy[len(self.axisitemy) - 1])
                    if linshi.index <= self.viewheight * 100 and linshi.index >= -self.viewheight * 100:
                        self.scene.addItem(linshi)
                    self.axisitemy.insert(0, linshi)
                    self.axisitemy.pop()





        elif self.start==2:
            for i in range(len(self.axisitemx)):
                if self.axisitemx[i].index>Pos.x():
                    break
            n= int(i-(len(self.axisitemx)-1)/2)
            span=self.axisitemx[1].index-self.axisitemx[0].index
            if n>0:
                for i in range(n):
                    linshi=GraphicsLineItem(self.axisitemx[len(self.axisitemx) - 1].index + span, -self.viewheight * 100,
                                            self.axisitemx[len(self.axisitemx) - 1].index + span, self.viewheight * 100)
                    linshi.setPen(QPen(QColor(10,100,240)))
                    linshi.setindex(self.axisitemx[len(self.axisitemx) - 1].index + span)
                    if self.axisitemx[0].index >= -self.viewwidth * 100 and self.axisitemx[0].index <= self.viewwidth * 100:
                        self.scene.removeItem(self.axisitemx[0])
                    if linshi.index <= self.viewwidth * 100 and linshi.index>= -100 * self.viewwidth:
                        self.scene.addItem(linshi)
                    self.axisitemx.append(linshi)
                    self.axisitemx.pop(0)
            elif n<0:
                for i in range(-n):
                    linshi=GraphicsLineItem(self.axisitemx[0].index - span, -self.viewheight * 100,
                                            self.axisitemx[0].index - span, self.viewheight * 100)
                    linshi.setPen(QPen(QColor(10,100,240)))
                    linshi.setindex(self.axisitemx[0].index - span)
                    if self.axisitemx[len(self.axisitemx) - 1].index >= -self.viewwidth * 100 \
                            and self.axisitemx[len(self.axisitemx) - 1].index <= self.viewwidth * 100:
                        self.scene.removeItem(self.axisitemx[len(self.axisitemx) - 1])
                    if linshi.index <= self.viewwidth * 100 and linshi.index>= -self.viewwidth*100:
                        self.scene.addItem(linshi)
                    self.axisitemx.insert(0, linshi)
                    self.axisitemx.pop()



            for i in range(len(self.axisitemy)):
                 if self.axisitemy[i].index > Pos.y():
                     break
            n = int(i - (len(self.axisitemx) - 1) / 2)
            span=self.axisitemy[1].index-self.axisitemy[0].index
            if n>0:
                for i in range(n):
                    linshi = GraphicsLineItem(-self.viewwidth * 100, self.axisitemy[len(self.axisitemy) - 1].index + span,
                                              self.viewwidth * 100, self.axisitemy[len(self.axisitemy) - 1].index + span)
                    linshi.setPen(QPen(QColor(10, 100, 240)))
                    linshi.setindex(self.axisitemy[len(self.axisitemy) - 1].index + span)
                    if self.axisitemy[0].index <= self.viewheight * 100 and self.axisitemy[
                        0].index >= -self.viewheight * 100:
                        self.scene.removeItem(self.axisitemy[0])
                    if linshi.index <= self.viewheight * 100 and linshi.index>= -self.viewheight*100:
                        self.scene.addItem(linshi)
                    self.axisitemy.append(linshi)
                    self.axisitemy.pop(0)
            elif n<0:
                for i in range(-n):
                    linshi = GraphicsLineItem(-self.viewwidth * 100,
                                              self.axisitemy[0].index - span,
                                              self.viewwidth * 100,
                                              self.axisitemy[0].index - span)
                    linshi.setPen(QPen(QColor(10, 100, 240)))
                    linshi.setindex(self.axisitemy[0].index - span)
                    if self.axisitemy[len(self.axisitemy) - 1].index >= -self.viewheight * 100 \
                            and self.axisitemy[len(self.axisitemy) - 1].index <= self.viewheight * 100:
                        self.scene.removeItem(self.axisitemy[len(self.axisitemy) - 1])
                    if linshi.index <= self.viewheight * 100 and linshi.index >= -self.viewheight * 100:
                        self.scene.addItem(linshi)
                    self.axisitemy.insert(0, linshi)
                    self.axisitemy.pop()

    def drawcircle(self, position):
        self.__dirty=True
        singlepoint = SinglePoint(position, 10)
        singlepoint.scale(1 / self.sumscale, 1 / self.sumscale)
        singlepoint.setToolTip(self.pointzuobiao(position))
        self.scene.addItem(singlepoint)
        self.circleitem.append(singlepoint)
        return singlepoint

    def keyPressEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            if event.key() == Qt.Key_R and self.origin:
                if self.addorigin:
                    self.start=0
                    if self.circleitem:
                        self.graphicsView.scale(1 / self.sumscale,
                                                1 / self.sumscale)
                        for i in self.circleitem:
                            i.scale(self.sumscale, self.sumscale)
                        self.graphicsView.centerOn(self.origin)
                        self.sumscale = 1
                    self.updateUi()
                    self.axis()

            if event.modifiers() & Qt.ShiftModifier:
                if event.key() == Qt.Key_C:
                    if self.addorigin:
                        self.fenmiao=~self.fenmiao
                        self.axis()


    def mousePressEvent(self, event):
            self.start=1
            pos = self.graphicsView.mapFromGlobal(event.globalPos())  # event.globalPos()与QCursor.pos()一样
            if 0 <= pos.x() <= self.viewwidth * 200 and 0 <= pos.y() <= self.viewwidth * 200:
                if self.addorigin:
                    if event.buttons() == Qt.LeftButton:
                        pass
                    if event.buttons() == Qt.RightButton:
                        self.__dirty = True
                        self.drawcircle(self.graphicsView.mapToScene(pos))
                        for i in self.circleitem:
                            print(self.pointzuobiao(i.pos()))
                    elif event.buttons() == Qt.MiddleButton:
                        pass
                    QGraphicsView.mousePressEvent(self.graphicsView, event)
                    # QGraphicsView::NoDrag ：忽略鼠标事件，不可以拖动。
                    # QGraphicsView::ScrollHandDrag ：光标变为手型，可以拖动场景进行移动。
                    # QGraphicsView::RubberBandDrag ：使用橡皮筋效果，进行区域选择，可以选中一个区域内的所有图形项。
                else:
                     QMessageBox.about(self, '提示', '''请先确定遇难位置''')

    def mouseReleaseEvent(self, event):
        if self.addorigin:
            pos = self.graphicsView.mapFromGlobal(event.globalPos())
            pos=self.graphicsView.mapToScene(pos)
            self.start=2
            self.updateUi(pos)
            self.axis()



    def deleteItem(self):
        item = self.scene.selectedItems()
        if len(item) == 0:
            return
        else:
            self.circleitem.remove(item[0])
            self.scene.removeItem(item[0])
            del item

    def wheelEvent(self, event):
        if self.addorigin:
            self.__dirty = True
            pos = self.graphicsView.mapFromGlobal(event.globalPos())
            pos = self.graphicsView.mapToScene(pos)
            self.sc = 1.001 ** event.delta()
            if self.sumscale < 0.01 and self.sc < 1:
                return
            if self.sumscale > 100 and self.sc > 1:
                return
            self.sumscale *= self.sc
            self.lastsc *= self.sc
            self.graphicsView.scale(self.sc, self.sc)
            for i in self.circleitem:
                i.scale(1 / self.sc, 1 / self.sc)
            if self.lastsc >= 2:
                self.updateUi(pos)
                self.lastsc = 1
                self.jishu += 1
            elif self.lastsc <= 0.5:
                self.updateUi(pos)
                self.lastsc = 1
                self.jishu -= 1
            self.axis()
        else:
            QMessageBox.about(self, '提示', '''请先选择飞机降落点''')



    def configure(self):
        configureexample = Configure.ConfDlg(self)
        configureexample.show()


    @pyqtSignature('')
    def on_pushButton_clicked(self):
        planepositionexample=planeposition.PlanePositionDlg(self)
        planepositionexample.show()
        self.connect(planepositionexample, SIGNAL('ppap(QString)'), self.p)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Mainwindow()
    form.show()
    app.exec_()
    form.Float()






