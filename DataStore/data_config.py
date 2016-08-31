from PyQt5 import QtWidgets, QtCore, QtGui


class ConfigData():
    def __init__(self, main_window):
        '''
        :type main_window: MainWindow.logic.MainWindowLogic
        :param main_window:
        '''
        self._font_size = 1
        self.main_window = main_window

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, value):
        value = int(value)
        if value == self._font_size:
            pass
        else:
            self._font_size = value