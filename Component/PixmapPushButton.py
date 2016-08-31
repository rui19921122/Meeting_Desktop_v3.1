from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPalette


class PixPushButton(QtWidgets.QPushButton):
    def __init__(self, pix, tooltip=None, width=50):
        super(PixPushButton, self).__init__()
        self.clearMask()
        pixmap = QtGui.QPixmap()
        pixmap.load(pix)
        self.setBackgroundRole(QPalette.Base)
        self.setIcon(QtGui.QIcon(pixmap))
        # self.setIconSize(QtCore.QSize(pixmap.width(), pixmap.height()))
        self.setIconSize(QtCore.QSize(width, width))
        self.setFixedSize(width,width)
        if tooltip:
            self.setToolTip(tooltip)
