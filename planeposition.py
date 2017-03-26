import ui_planeposition
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
class PlanePositionDlg(QDialog, ui_planeposition.Ui_planeposition):
    def __init__(self, parent=None):
        super(PlanePositionDlg, self).__init__(parent)
        self.setupUi(self)
        self.weidu=0
        self.jindu=0
        self.connect(self.ppweidu1spinBox, SIGNAL('valueChanged(int)'), self.correspondent)
        self.connect(self.ppweidu2spinBox, SIGNAL('valueChanged(int)'), self.correspondent)
        self.connect(self.ppweidu3spinBox, SIGNAL('valueChanged(double)'), self.correspondent)
        self.connect(self.ppjindu1spinBox, SIGNAL('valueChanged(int)'), self.correspondent3)
        self.connect(self.ppjindu2spinBox, SIGNAL('valueChanged(int)'), self.correspondent3)
        self.connect(self.ppjindu3spinBox, SIGNAL('valueChanged(double)'), self.correspondent3)
        self.connect(self.ppweidudoubleSpinBox, SIGNAL('valueChanged(double)'), self.correspondent2)
        self.connect(self.ppjindudoubleSpinBox, SIGNAL('valueChanged(double)'), self.correspondent4)

    def correspondent(self):
        a = self.ppweidudoubleSpinBox.value() % 60
        b = int(self.ppweidudoubleSpinBox.value() / 60) % 60
        c = int(self.ppweidudoubleSpinBox.value() / 60 / 60)
        if c!=self.ppweidu1spinBox.value() or b!=self.ppweidu2spinBox.value() or a!=self.ppweidu3spinBox.value():
            self.weidu=self.ppweidu1spinBox.value()+self.ppweidu2spinBox.value()/60\
                +self.ppweidu3spinBox.value()/3600
            self.ppweidudoubleSpinBox.setValue(self.weidu)
        else:
            return


    def correspondent3(self):
        a = self.ppjindudoubleSpinBox.value() % 60
        b = int(self.ppjindudoubleSpinBox.value() / 60) % 60
        c = int(self.ppjindudoubleSpinBox.value() / 60 / 60)
        if c!=self.ppjindu1spinBox.value() or b!=self.ppjindu2spinBox.value() or a!=self.ppjindu3spinBox.value():
            self.jindu=self.ppjindu1spinBox.value()+self.ppjindu2spinBox.value()/60\
                +self.ppjindu3spinBox.value()/3600
            self.ppjindudoubleSpinBox.setValue(self.jindu)
        else:
            return


    def correspondent2(self):
        if abs(self.weidu-self.ppweidudoubleSpinBox.value())<10e-6:
            a = int(self.weidu)
            b = int(self.weidu*60-a*60)
            c = self.weidu*3600-a*3600-b*60
            if c!=self.ppweidu1spinBox.value() or b!=self.ppweidu2spinBox.value() or a!=self.ppweidu3spinBox.value():
                    self.ppweidu1spinBox.setValue(a)
                    self.ppweidu2spinBox.setValue(b)
                    self.ppweidu3spinBox.setValue(c)
            else:
                return
        else:
            a = int(self.ppweidudoubleSpinBox.value())
            b = int(self.ppweidudoubleSpinBox.value()*60-a*60)
            c = self.ppweidudoubleSpinBox.value()*3600-a*3600-b*60
            if c!=self.ppweidu1spinBox.value() or b!=self.ppweidu2spinBox.value() or a!=self.ppweidu3spinBox.value():
                    self.ppweidu1spinBox.setValue(a)
                    self.ppweidu2spinBox.setValue(b)
                    self.ppweidu3spinBox.setValue(c)
            else:
                return

    def correspondent4(self):
        if abs(self.jindu-self.ppjindudoubleSpinBox.value())<10e-6:
            a = int(self.jindu)
            b = int(self.jindu * 60 - a * 60)
            c = self.jindu * 3600 - a * 3600 - b * 60
            if c != self.ppjindu1spinBox.value() or b != self.ppjindu2spinBox.value() or a != self.ppjindu3spinBox.value():
                self.ppjindu1spinBox.setValue(a)
                self.ppjindu2spinBox.setValue(b)
                self.ppjindu3spinBox.setValue(c)
            else:
                return
        else:
            a = int(self.ppjindudoubleSpinBox.value())
            b = int(self.ppjindudoubleSpinBox.value()*60-a*60)
            c = self.ppjindudoubleSpinBox.value()*3600-a*3600-b*60
            if c!=self.ppjindu1spinBox.value() or b!=self.ppjindu2spinBox.value() or a!=self.ppjindu3spinBox.value():
                self.ppjindu1spinBox.setValue(a)
                self.ppjindu2spinBox.setValue(b)
                self.ppjindu3spinBox.setValue(c)
            else:
                return
        

    @pyqtSignature("")
    def on_ppokpushButton_clicked(self):
        weidu=self.ppweiducomboBox.currentText()
        jingdu=self.ppjinducomboBox.currentText()
        a = self.ppweidu1spinBox.text()[:-1]
        b = self.ppweidu2spinBox.text()[:-1]
        c = self.ppweidu3spinBox.text()[:-2]
        d = self.ppjindu1spinBox.text()[:-1]
        e = self.ppjindu2spinBox.text()[:-1]
        f = self.ppjindu3spinBox.text()[:-2]
        self.emit(SIGNAL("ppap(QString)"), '%s,%s,%s%s-%s,%s,%s%s'%(a, b, c, weidu, d, e, f, jingdu))
        self.close()

    def on_ppcancelpushButton_clicked(self):
        self.close()

    
if __name__=='__main__':
    app = QApplication(sys.argv)
    form = PlanePositionDlg()
    form.show()
    app.exec_()
