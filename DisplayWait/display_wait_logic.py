import os
from CallOverScreen.call_over_logic import CallOverScreenWidget
from collections import OrderedDict

import datetime

from Exception.figure_collect_failed import FigureCollectFailed

from PyQt5 import QtCore, QtWidgets, QtMultimedia, QtGui

from HttpRequest import HttpRequest
from .Display import Ui_DisplayWorker


class AlignHCenterTableItem(QtWidgets.QTableWidgetItem):
    def __init__(self, text):
        super(AlignHCenterTableItem, self).__init__()
        self.setText(text)
        self.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)


class DisplayWaitLogic(QtWidgets.QWidget, Ui_DisplayWorker):
    def __init__(self, parent, main_window):
        '''
        :type main_window: MainWindow.logic.MainWindowLogic
        :param parent:
        :param main_window:
        '''
        super(DisplayWaitLogic, self).__init__(parent)
        self.main_window = main_window
        self.setupUi(self)
        self.tableWidget.setRowCount(0)
        self.refresh_worker_status()

    def refresh_worker_status(self):
        request = HttpRequest(parent=self.main_window, url='api/call_over/get-call-over-person/', method='get')
        if self.main_window.store.attend_table and self.main_window.store.attend_table['lock']:
            request.success.connect(lambda data: self.handle_data_refresh(data['attend']))
        else:
            request.success.connect(lambda data: self.handle_initial_data(data['attend']))
        request.failed.connect(lambda message: self.main_window.warn.add_warn(message))
        request.start()

    def handle_data_refresh(self, data):
        """
        刷新出勤表
        :param data:
        :return:
        """
        persons = data['person']
        if data['lock']:
            '''
            如果表未锁定，因可能存在增删人员情况，故重新渲染整个页面
            '''
            for i in persons:
                if i['id'] in self.main_window.store.worker_status:
                    lines = self.main_window.store.worker_status[i['id']]
                    lines[0].setText(i['worker'])
                    lines[1].setText(i['position'])
                    lines[2].setText('是' if i['study'] else '否'),
                    lines[3].setText(self.render_data(i['checked'])),
                else:
                    self.main_window.store.worker_status[i['id']] = [
                        AlignHCenterTableItem(i['worker']),
                        AlignHCenterTableItem(i['position']),
                        AlignHCenterTableItem('是' if i['study'] else '否'),
                        AlignHCenterTableItem(self.render_data(i['checked'])),
                    ]
                    row = self.tableWidget.rowCount()
                    self.tableWidget.setRowCount(row + 1)
                    for index, d in enumerate(self.main_window.store.worker_status[i['id']]):
                        self.tableWidget.setItem(row, index, d)
        else:
            self.tableWidget.setRowCount(0)
            self.main_window.store.worker_status = OrderedDict()
            for i in persons:
                self.main_window.store.worker_status[i['id']] = [
                    AlignHCenterTableItem(i['worker']),
                    AlignHCenterTableItem(i['position']),
                    AlignHCenterTableItem('是' if i['study'] else '否'),
                    AlignHCenterTableItem(self.render_data(i['checked'])),
                ]
                row = self.tableWidget.rowCount()
                self.tableWidget.setRowCount(row + 1)
                for index, d in enumerate(self.main_window.store.worker_status[i['id']]):
                    self.tableWidget.setItem(row, index, d)

    def render_data(self, data: str):
        if data:
            return data.split('T')[-1]
        else:
            return '未打点'

    def handle_initial_data(self, data):
        try:
            self.BeginButton.disconnect()
        except:
            pass
        self.main_window.store.attend_table = data
        attend = self.main_window.store.attend_table
        text = "{}{}日{}点名会".format(
            attend.get("department"),
            attend.get("date"),
            "白班" if attend.get("day_number") == '1' else "夜班"
        )
        self.label.setText('''
        <html><head/><body><p><span style=" font-size:18pt; font-weight:600;" > {} < / span > < / p > < / body > < / html >
        '''.format(text)
                           )
        if not attend.get('lock', False):
            self.BeginButton.clicked.connect(self.handle_begin_call_over_button_clicked)
        else:
            box = QtWidgets.QMessageBox()
            answer = box.information(self, "警告", "考勤表已经锁定，点击确定按钮后即开始录影,点取消将会退出",
                                     QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.No)
            if answer == QtWidgets.QMessageBox.Ok:
                self.BeginButton.setText("查看班前预想")
                self.open_camera_and_audio_and_figure()
                try:
                    self.BeginButton.disconnect()
                except:
                    pass
                self.BeginButton.clicked.connect(self.look_info)
            else:
                self.main_window.close()
        self.handle_data_refresh(data=attend)

    def handle_begin_call_over_button_clicked(self):
        message_box = QtWidgets.QMessageBox.warning(self, '警告', '锁定点名表后将无法修改出勤人员，确定么',
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if message_box == QtWidgets.QMessageBox.Yes:
            res = HttpRequest(parent=self.main_window,
                              url='api/v2/call_over/lock-call-over-person/',
                              method='post',
                              data={'number': self.main_window.store.attend_table.get('id')})
            res.success.connect(self.begin_call_over)
            res.failed.connect(lambda message: self.main_window.warn.add_warn(message))
            res.start()
        else:
            pass

    def begin_call_over(self):
        try:
            self.BeginButton.disconnect()
        except:
            pass
        self.main_window.store.attend_table['lock'] = True
        self.BeginButton.setText("查看班前预想")
        self.open_camera_and_audio_and_figure()
        # try:
        #     self.BeginButton.disconnect()
        # except:
        #     pass
        self.BeginButton.clicked.connect(self.look_info)
        self.BeginButton.click()

    def open_camera_and_audio_and_figure(self):
        if self.main_window.store.device_figure.has_device():
            self.main_window.warn.add_warn("开始采集指纹")
            self.main_window.store.timer_figure = QtCore.QTimer(self.main_window)
            self.main_window.store.timer_figure.timeout.connect(self.check_figure)
            self.check_figure()
        else:
            self.main_window.warn.add_warn("未找到指纹仪", type='error')
        if self.main_window.store.device_mic.current_mic:
            try:
                self.main_window.store.device_mic.recorder_path = os.path.join(os.getcwd(), 'audio.wav')
                self.main_window.store.device_mic.start_record()
                self.main_window.warn.add_warn("开始录音")
            except Exception as error:
                self.main_window.warn.add_warn("录音失败", type='error')
        else:
            self.main_window.warn.add_warn("未找到或设置录音设备，录音失败", type='error')
        self.main_window.store.device_camera.path = os.path.join(os.getcwd(),'i.avi')
        self.main_window.store.device_camera.start_capture()

    def check_figure(self, next_=1000):
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
                request.success.connect(lambda message: self.refresh_worker_status())
                request.failed.connect(lambda message: self.main_window.warn.add_warn(message, type='error'))
                request.start()
            except FigureCollectFailed:
                self.main_window.warn.add_warn("采集指纹失败", type='error')
            finally:
                self.main_window.store.timer_figure.start()
        else:
            self.main_window.store.timer_figure.start(next_)

    def look_info(self):
        """
        进入下一步
        :return:
        """
        # try:
        self.BeginButton.disconnect()
        # except:
        #     pass
        request = HttpRequest(url='api/call_over/get-call-over-text/', method='get', parent=self.main_window)
        request.success.connect(lambda data: self.change_into_view(data=data))
        request.failed.connect(lambda message: self.main_window.warn.add_warn(message, type='error'))
        request.start()
        # f = CallOverScreenWidget(parent=self.main_window, data={}, main_window=self.main_window)
        # self.main_window.stacked_layout.addWidget(f)
        # self.close()

    def change_into_view(self, data):
        print(data)
        self.close()
        f = CallOverScreenWidget(parent=self.main_window, data=data, main_window=self.main_window)
        self.main_window.stacked_layout.addWidget(f)

    def close(self):
        try:
            self.main_window.store.timer_figure.stop()
            self.main_window.store.timer_figure.disconnect()
        except:
            pass
        finally:
            super(DisplayWaitLogic, self).close()
