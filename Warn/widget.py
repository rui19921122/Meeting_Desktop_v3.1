from PyQt5 import QtWidgets, QtCore, QtGui
from functools import partial


class Warning(QtWidgets.QWidget):
    def __init__(self, parent=None, main_window=None):
        super(Warning, self).__init__()
        self.setParent(parent)
        self.parent = parent
        self.main_window = main_window
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setDirection(QtWidgets.QVBoxLayout.BottomToTop)
        self.setLayout(self.main_layout)
        self.main_layout.setAlignment(QtCore.Qt.AlignTop)
        self.setMaximumWidth(300)

    def add_warn(self, message, type='warn', delay=3):
        label = QtWidgets.QLabel()
        label.setAutoFillBackground(True)
        if type == 'warn':
            color = '#1DFFDF'
        elif type == 'error':
            color = 'red'
        else:
            color = '#1DFFDF'
        label.setStyleSheet('background-color:{};border-radius:10px'.format(color))
        label.setText(message)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setMaximumHeight(200)
        label.setMinimumHeight(200)
        label.setWordWrap(True)
        self.main_layout.addWidget(label)
        timer = QtCore.QTimer(self.main_window)
        timer.start(delay * 1000)
        timer.timeout.connect(partial(self.remove_warn, timer=timer, label=label))
        assert isinstance(self.parent, QtWidgets.QWidget)
        self.resize(300, self.main_layout.count() * 200)
        self.move(0, 20)
        self.parent.layout().setCurrentWidget(self)
        # todo 检测是否有可能出现bug
        self.show()

    def remove_warn(self, timer: QtCore.QTimer, label: QtWidgets.QLabel):
        # todo 解耦所有timer
        timer.deleteLater()
        label.setParent(None)
        label.destroy()
        self.resize(300, self.main_layout.count() * 200)
        self.move(0, 20)
        if self.main_layout.count() == 0:
            self.hide()
