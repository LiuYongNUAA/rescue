from PyQt4.QtGui import *
from PyQt4.QtCore import *
class SinglePoint(QGraphicsItem):
    def __init__(self, position=None, s=10, color=Qt.black):
        super(SinglePoint, self).__init__()
        Rect = QRectF(-s, -s, s, s)
        self.Rect = Rect
        self.position = position
        self.falseposition = position
        self.color = color
        self.setPos(self.position)
        self.people = 1
        self.size=s
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
        self.setSelected(False)
        self.setFocus()
        self.index=None


    def boundingRect(self):
        return self.Rect

    def shape(self):
        path = QPainterPath()
        path.addEllipse(self.Rect)
        return path

    def paint(self, painter, option, widget=None):
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self.color))
        painter.drawEllipse(self.Rect)

    def itemChange(self, change, variant):
        if self.isSelected():
            self.color = Qt.red
            self.setScale(2)
            self.setPos(self.falseposition.x()+self.size,self.falseposition.y()+self.size)
        else:
            self.color = Qt.black
            self.setScale(1)
            self.setPos(self.position)
        return QGraphicsItem.itemChange(self, change, variant)


