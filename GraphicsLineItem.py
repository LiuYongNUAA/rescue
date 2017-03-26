from PyQt4.QtCore import *
from PyQt4.QtGui import *
class GraphicsLineItem(QGraphicsLineItem):
    def _init_(self, parent=None):
        super(GraphicsTextItem, self).__init__(parent)
        self.index=None

    def setindex(self, jishu=None):
        self.index=jishu
