from PyQt5 import QtWidgets, QtCore


class BaseWidget(QtWidgets.QWidget):
    def __init__(self, widget: QtWidgets.QWidget, parent=None):
        super(BaseWidget, self).__init__(QWidget_parent=parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)