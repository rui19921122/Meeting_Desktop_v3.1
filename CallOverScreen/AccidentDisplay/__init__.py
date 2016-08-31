from PyQt5 import QtGui, QtCore, QtWidgets
from .AccidentDisplay import Ui_Form


class AccidentDisplay(QtWidgets.QWidget, Ui_Form):
    def __init__(self, index, count, content, files, font_size, main_window):
        """
        :type main_window: MainWindow.logic.MainWindowLogic

        :param index:
        :param count:
        :param content:
        :param files:
        :param font_size:
        :param main_window:
        """
        super(AccidentDisplay, self).__init__()
        self.setupUi(self)
        self.TextLabel.setText('''
            <html><head/><body><p><span style="font-size:{}pt;">规章文件、事故案例学习(第{}条,共{}条)</span></p></body></html>
        '''.format(font_size, index + 1, count))
        self.textBrowser.setText(
            '''<html><head/><body><p><span style="font-size:{}pt;">{}</span></p></body></html>'''.format(font_size,
                                                                                                        content))
        if len(files) == 0:
            pass
        else:
            for file in files:
                widget = QtWidgets.QListWidgetItem()
                widget.setText(file['filename'])
                widget.setData(0, file['filename'])
                widget.setData(1, file['file'])
                self.listWidget.addItem(widget)
            self.listWidget.doubleClicked.connect(self.handleClicked)

    def handleClicked(self, item):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(item.data(1)))
