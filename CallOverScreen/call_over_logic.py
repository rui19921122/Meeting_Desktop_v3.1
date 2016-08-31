import ctypes
from EndCallScreen.EndCallScreenLogic import EndCallScreenLogic
import os

from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia

from Exception.figure_collect_failed import FigureCollectFailed
from .AccidentDisplay import AccidentDisplay
from .CallOverScreen import Ui_Form
from HttpRequest.requests import HttpRequest

try:
    from mainWindow import MainWindow
except:
    pass

from functools import partial


class CallOverScreenWidget(QtWidgets.QWidget, Ui_Form):
    over = QtCore.pyqtSignal(int)
    figure_checked = QtCore.pyqtSignal(bytes)
    worker_data = QtCore.pyqtSignal(dict)

    def __init__(self, parent, data: dict, main_window):
        """
        :type main_window: MainWindow.logic.MainWindowLogic
        """
        super(CallOverScreenWidget, self).__init__()
        self.setParent(parent)
        self.main_window = main_window
        self.data = data['data']
        self.call_over_id = data['pk']
        self.parent = parent
        self.setupUi(self)
        self.process_data(font_size=self.main_window.store.config_data.font_size)
        self.set_up_devices()
        self.Back.clicked.connect(self.handleBack)
        # self.Back.setDisabled(True)
        # if self.DisplayLayout.count() <= 1:
        #     self.Forward_2.setDisabled(True)
        self.Forward_2.clicked.connect(self.handleForward)
        self.main_window.font_size_change.connect(lambda value: self.process_data(value))
        # self.worker_data.connect(lambda data: self.parent.warn.add_warn('{}已签到'.format(data['people'])))

    def set_up_devices(self):
        """
        鉴于视频与音频设备在点名阶段已启用，这里仅提供指纹仪界面
        :return:
        """
        self.main_window.store.timer_figure = QtCore.QTimer()
        self.main_window.store.timer_figure.timeout.connect(self.check_figure)
        self.main_window.store.timer_figure.start(5000)

    def check_figure(self, next_=3000):
        """
        :param next_: 采集指纹完毕后下一次开始的时间
        :return:
        """
        self.main_window.store.timer_figure.stop()
        if self.main_window.store.device_figure.pressed():
            try:
                tem = self.main_window.store.device_figure.get_figure(quiet=False)
                request = HttpRequest(url="api/call_over/post-figure/",
                                      data={
                                          'figure_data': tem,
                                          'number': self.main_window.store.attend_table['id']

                                      }, method='post', parent=self.main_window)
                request.success.connect(lambda message: self.main_window.warn.add_warn(message.get("people") + "已打点"))
                request.failed.connect(lambda message: self.main_window.warn.add_warn(message, type='error'))
                request.start()
            except FigureCollectFailed:
                self.main_window.warn.add_warn("采集指纹失败", type='error')
            finally:
                self.main_window.store.timer_figure.start()
        else:
            self.main_window.store.timer_figure.start(next_)

    def image_captured(self, capture_id, data):
        res = HttpRequest(method='post', parent=self.parent,
                          url='api/v2/upload/call-over-image/{}'.format(self.call_over_id),
                          files={'file': open(data, 'rb')}
                          )
        res.failed.connect(lambda message: print(message))
        res.success.connect(lambda _data: os.remove(data))
        res.start()

    def process_data(self, font_size):
        count = self.DisplayLayout.count()
        if count >= 1:
            self.DisplayLayout.close()
            self.DisplayLayout = QtWidgets.QStackedWidget()
            self.verticalLayout_2.insertWidget(2, self.DisplayLayout)
        self.Back.setDisabled(True)
        self.is_end = False
        data = self.data
        classPlanData = data['class_plan']
        dayDetail = classPlanData['day_detail']
        font = QtGui.QFont()
        font.setPointSize(font_size)
        if len(dayDetail) > 0:
            classPlan = QtWidgets.QTableWidget()
            classPlan.setFont(font)
            classPlan.setColumnCount(4)
            classPlan.setHorizontalHeaderLabels(['序号', '名称', '内容', '涉及部门'])
            classPlan.horizontalHeader().setStretchLastSection(True)
            classPlan.verticalHeader().setVisible(False)
            width = self.DisplayLayout.width()
            classPlan.setColumnWidth(0, int(width * 0.10))
            classPlan.setColumnWidth(1, int(width * 0.15))
            classPlan.setColumnWidth(2, int(width * 0.40))
            classPlan.setColumnWidth(3, int(width * 0.15))
            row_count = 0
            for i in dayDetail:
                publishDetail = i['publish_detail']
                row_count += len(publishDetail)
            classPlan.setRowCount(row_count)
            row = 0
            for i in dayDetail:
                publishDetail = i['publish_detail']
                if len(publishDetail) >= 1:
                    classPlan.setItem(row, 1, QtWidgets.QTableWidgetItem(i['style']))
                    classPlan.setSpan(row, 1, row + len(publishDetail), 1)
                    classPlan.setItem(row, 3, QtWidgets.QTableWidgetItem(i['department']))
                    classPlan.setSpan(row, 3, row + len(publishDetail), 3)
                    for detail in publishDetail:
                        classPlan.setItem(row, 2, QtWidgets.QTableWidgetItem(detail['detail']))
                        classPlan.setItem(row, 0, QtWidgets.QTableWidgetItem(str(row + 1)))
                        row += 1
        else:
            classPlan = QtWidgets.QLabel()
            classPlan.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            classPlan.setText('''''''<p style="font-size:{}px">本日无班计划录入'''.format(font_size))
        self.DisplayLayout.addWidget(classPlan)
        accident = data['accident']
        assert isinstance(accident, list)
        if len(accident) > 0:
            for i in accident:
                new = AccidentDisplay(accident.index(i), len(accident), i['content'], i['files'], font_size,
                                      main_window=self.main_window)
                new.setFont(font)
                self.DisplayLayout.addWidget(new)
        else:
            accidentWidget = QtWidgets.QLabel()
            accidentWidget.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            accidentWidget.setText('''''''<p style="font-size:{}px">本日无文件通报</p>'''.format(font_size))
            self.DisplayLayout.addWidget(accidentWidget)
        if self.DisplayLayout.count() <= 1:
            self.Forward_2.setDisabled(True)

    def handleBack(self):
        self.DisplayLayout.setCurrentIndex(self.DisplayLayout.currentIndex() - 1)
        self.render_button(self.DisplayLayout.currentIndex(), self.DisplayLayout.count())

    def end(self):
        def handle_success():
            self.main_window.store.device_mic.end_record()
            self.main_window.store.device_camera.end_capture()
            if self.main_window.store.timer_figure and self.main_window.store.timer_figure.isActive():
                self.main_window.store.timer_figure.stop()
            end = EndCallScreenLogic(main_window=self.main_window)
            self.main_window.stacked_layout.addWidget(end)
            self.close()

        request = HttpRequest(url="api/call_over/end-call-over", method='post', parent=self.main_window)
        request.success.connect(handle_success)
        request.failed.connect(lambda message: self.main_window.warn.add_warn(message, type='error'))
        request.start()

    def handleForward(self):
        if self.is_end:
            self.end()
        else:
            self.DisplayLayout.setCurrentIndex(self.DisplayLayout.currentIndex() + 1)
        self.render_button(self.DisplayLayout.currentIndex(), self.DisplayLayout.count())

    def render_button(self, index, length):
        if index <= 0:
            self.Back.setDisabled(True)
        else:
            self.Back.setDisabled(False)
        if index == length - 1:
            self.is_end = True
            self.Forward_2.setText("结束点名")
        else:
            self.Forward_2.setText("后一条")
            self.is_end = False
