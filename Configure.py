import UI_Configure
import sys
from configobj import ConfigObj
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class ConfDlg(QDialog,UI_Configure.Ui_Configure):
    def __init__(self, parent=None):
        super(ConfDlg, self).__init__(parent)
        self.setupUi(self)
        self.MenDWLdoubleSpinBox.setValue(1.14)
        self.MenCWLdoubleSpinBox.setValue(0.54)
        self.MenDWLerrordoubleSpinBox.setValue(5.56)
        self.MenCWLerrordoubleSpinBox.setValue(4.34)
        self.BoatDWLdoubleSpinBox.setValue(3.13)
        self.BoatDWLerrordoubleSpinBox.setValue(4.84)
        self.BoatCWLdoubleSpinBox.setValue(1.21)
        self.BoatCWLerrordoubleSpinBox.setValue(3.10)
        self.Boat2DWLdoubleSpinBox.setValue(1.25)
        self.Boat2DWLerrordoubleSpinBox.setValue(3.96)
        self.Boat2CWLdoubleSpinBox.setValue(0.19)
        self.Boat2CWLerrordoubleSpinBox.setValue(1.14)
        self.connect(self.OKbutton, SIGNAL('clicked()'), self.SetConfig)

    def SetConfig(self):
        config = ConfigObj()
        config.filename = 'Config'
        config['MenDWL'] = self.MenDWLdoubleSpinBox.value()
        config['MenCWL'] = self.MenCWLdoubleSpinBox.value()
        config['MenDWLerror'] = self.MenDWLerrordoubleSpinBox.value()
        config['MenCWLerror'] = self.MenCWLerrordoubleSpinBox.value()
        config['LifeBoatDWL'] = self.BoatDWLdoubleSpinBox.value()
        config['LifeBoatCWL'] = self.BoatCWLdoubleSpinBox.value()
        config['LifeBoatDWLerror'] = self.BoatDWLerrordoubleSpinBox.value()
        config['LifeBoatCWLerror'] = self.BoatCWLerrordoubleSpinBox.value()
        config['ShipDWL'] = self.Boat2DWLdoubleSpinBox.value()
        config['ShipCWL'] = self.Boat2CWLdoubleSpinBox.value()
        config['ShipDWLerror'] = self.Boat2DWLerrordoubleSpinBox.value()
        config['ShipCWLerror'] =self.Boat2CWLerrordoubleSpinBox.value()
        config.write()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dig = ConfDlg()
    dig.show()
    app.exec_()
