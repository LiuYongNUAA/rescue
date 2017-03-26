from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
class GraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setRenderHint(QPainter.Antialiasing)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        # NoAnchor, AnchorViewCenter, AnchorUnderMouse代表图形变换时的基准点
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        # 图像变化时可以最小程度改变图像以降低性能消耗
        self.setFocusPolicy(Qt.StrongFocus)
        # Qt::TabFocus	0x1	 接受Tab键焦点/
        # Qt::ClickFocus 0x2	接受鼠标单击做焦点
        # Qt::StrongFocus	TabFocus | ClickFocus | 0x8	接受Tab键和鼠标单击做焦点
        # Qt::WheelFocus	StrongFocus | 0x4	 滑轮作为焦点选中事件
        # Qt::NoFocus	0	不接受焦点
        self.setMouseTracking(False)
        # 如果鼠标跟踪失效（默认），当鼠标被移动的时候只有在至少一个鼠标按键被按下时，这个窗口部件才会接收鼠标移动事件。
        # 如果鼠标跟踪生效，如果没有按键被按下，这个窗口部件也会接收鼠标移动事件。
        self.aspectLocked = False
        self.setRenderHints(self.renderHints() | QPainter.Antialiasing)

    def mouseReleaseEvent(self, event):
        QGraphicsView.mouseReleaseEvent(self, event)
        event.ignore()  # 这一步非常重要，否则release会被graphicsview吸收，传不到scene那边了

    def wheelEvent(self, event):
        event.ignore()

if __name__ == '__main__':
    app =  QApplication(sys.argv)
    graphics = GraphicsView()
    graphics.setGeometry(0,0,800,600)
    graphics.show()
    app.exec_()
