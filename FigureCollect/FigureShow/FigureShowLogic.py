import sys

from Exception.figure_collect_failed import FigureCollectFailed
from HttpRequest import HttpRequest
import requests
from PyQt5 import QtWidgets, QtCore
from . import FigureShow
from .figurebutton import FigureButton
from functools import partial

figure_map = {
    'l1': '左手大拇指',
    'l2': '左手食指',
    'l3': '左手中指',
    'l4': '左手无名指',
    'l5': '左手小拇指',
    'r1': '右手大拇指',
    'r2': '右手食指',
    'r3': '右手中指',
    'r4': '右手无名指',
    'r5': '右手小拇指'
}


class FiguresShowLogic(QtWidgets.QDialog, FigureShow.Ui_Dialog):
    _close = QtCore.pyqtSignal()

    def __init__(self, data, id, parent, main_window):
        '''
        :type main_window: MainWindow.logic.MainWindowLogic
        :param parent:
        :param main_window:
        '''
        super(FiguresShowLogic, self).__init__(parent)
        self.main_window = main_window
        self._close.connect(parent.get_worker_table)
        self.data = data
        self.id = id  # 职工id
        figure_data = data['figures']
        self.setupUi(self)
        self.refresh_status(figure_data=self.data['figures'])

    def closeEvent(self, QCloseEvent):
        self._close.emit()

    def refresh_status(self, figure_data):
        for button in [self.l1, self.l2, self.l3, self.l4, self.l5, self.r1, self.r2, self.r3, self.r4, self.r5]:
            name = button.objectName()
            if figure_map[name] in figure_data:
                try:
                    button.disconnect()
                except:
                    pass
                button.setStyleSheet("background-image:url(:/logo/resource/png/Had.jpg);")
                button.clicked.connect(partial(self.handleHadFigureButtonClicked, figure_map[name]))
            else:
                try:
                    button.disconnect()
                except:
                    pass
                button.setStyleSheet("background-image:url(:/logo/resource/png/NotHad.jpg);")
                button.clicked.connect(partial(self.handleNotHadFigureButtonClicked, figure_map[name]))

    def handleHadFigureButtonClicked(self, name):
        if QtWidgets.QMessageBox.warning(self, "警告",
                                         '职工{}的{}已经录有指纹，此操作将删除其指纹，是否确定?'.format(self.data.get('name'),
                                                                                name),
                                         QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
                                         ) == QtWidgets.QMessageBox.Yes:
            request = HttpRequest(parent=self.main_window,
                                  method='delete',
                                  data={'id': self.id, 'name': name},
                                  url='api/worker/figure-post/'
                                  )
            request.success.connect(lambda data: self.refresh_status(figure_data=data['figures']))
            request.failed.connect(lambda message: self.main_window.warn.add_warn(message, type='error'))
            request.start()

    def handleNotHadFigureButtonClicked(self, name):
        if self.main_window.store.device_figure.has_device():
            try:
                value = self.main_window.store.device_figure.get_figure_template()
                request = HttpRequest(parent=self.main_window, url='api/worker/figure-post/',
                                      data={'id': self.id,
                                            'name': name,
                                            'value': value
                                            }, method='post')
                request.success.connect(lambda data: self.refresh_status(data['figures']))
                request.failed.connect(lambda message: self.main_window.warn.add_warn(message=message, type='error'))
                request.start()
            except FigureCollectFailed:
                QtWidgets.QMessageBox.warning(self, "错误",
                                              '采集指纹失败',
                                              QtWidgets.QMessageBox.Yes
                                              )

        else:
            QtWidgets.QMessageBox.warning(self, "错误",
                                          '未找到指纹仪',
                                          QtWidgets.QMessageBox.Yes
                                          )
