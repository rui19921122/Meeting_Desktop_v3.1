from PyQt5 import QtWidgets, QtCore


class FigureButton(QtWidgets.QPushButton):
    deleteSingle = QtCore.pyqtSignal(object)
    getSinge = QtCore.pyqtSignal()

    def __init__(self, bool, parent):
        super(FigureButton, self).__init__()
        self.id = id
        self.bool = bool

    def setUpUi(self):
        self.setText('')
        if self.bool:
            self.r5.setStyleSheet("background-image:url(:/FigureImage/resource/Had.jpg);")
        else:
            self.r5.setStyleSheet("background-image:url(:/FigureImage/resource/notHad.jpg);")

    def click(self):
        pass
