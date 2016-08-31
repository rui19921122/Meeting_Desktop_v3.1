import requests
from PyQt5 import QtWidgets, QtCore

from FigureCollect.FigureShow.FigureShowLogic import FiguresShowLogic
from HttpRequest import HttpRequest
from .FigureCollect import Ui_Form


class TableItem(QtWidgets.QTableWidgetItem):
    def __init__(self, text):
        super(TableItem, self).__init__()
        self.setText(text)
        self.setTextAlignment(QtCore.Qt.AlignCenter)


class FigureCollectionLogic(QtWidgets.QWidget, Ui_Form):
    _update_table_widget = QtCore.pyqtSignal(object)

    def __init__(self, main_window):
        '''
        :type main_window: MainWindow.logic.MainWindowLogic
        :param parent:
        :param main_window:
        '''
        super(FigureCollectionLogic, self).__init__()
        self._update_table_widget.connect(self.update_table_widget)
        self.main_window = main_window
        self.setupUi(self)
        self.get_worker_table()
        self.tableWidget.cellDoubleClicked.connect(self.cellDoubleClicked)
        self.tableWidget.verticalHeader().hide()
        self.departmentLabel.setText('')
        self.personLabel.setText('')

    def get_worker_table(self):
        request = HttpRequest(parent=self.main_window, method='get', url='api/worker/worker')
        request.success.connect(lambda data: self.update_table_widget(data))
        request.failed.connect(lambda data: self.main_window.warn.add_warn(data, type='error'))
        request.start()

    def update_table_widget(self, obj):
        self.tableWidget.setRowCount(len(obj))
        row = 0
        for person in obj:
            self.tableWidget.setItem(row, 0, TableItem(str(person['id'])))
            self.tableWidget.setItem(row, 1, TableItem(person['name']))
            self.tableWidget.setItem(row, 2, TableItem(str(person['class_number']) + '班'))
            self.tableWidget.setItem(row, 3, TableItem('是' if person['is_study'] else '否'))
            self.tableWidget.setItem(row, 4, TableItem(str(len(person['figures']))))
            row += 1

    def cellDoubleClicked(self, row, col):
        item = self.tableWidget.item(row, 0)
        """:type item:QtWidgets.QTableWidgetItem"""

        def handle_success(data):
            print(111)
            f = FiguresShowLogic(id=person_id, data=data, parent=self,
                                 main_window=self.main_window)
            f._close.connect(self.get_worker_table)
            f.exec_()

        person_id = item.text()
        request = HttpRequest(url='api/worker/worker/{}'.format(person_id), method='get', parent=self.main_window)
        request.success.connect(handle_success)
        request.failed.connect(lambda message: self.main_window.warn.add_warn(message, type="error"))
        request.start()
