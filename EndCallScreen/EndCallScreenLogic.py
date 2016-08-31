import sys

import datetime
from PyQt5 import QtCore, QtWidgets, QtGui

from HttpRequest import HttpRequest
from .end import Ui_Form
import requests
import os
import subprocess as sp


class FFMPEG_THREAD(QtCore.QThread):
    success = QtCore.pyqtSignal()
    failed = QtCore.pyqtSignal()

    def __init__(self, args, parent):
        super(FFMPEG_THREAD, self).__init__()
        self.setParent(parent)
        self.args = args

    def run(self):
        try:
            f = sp.check_call(self.args)
            self.success.emit()
        except:
            self.failed.emit()


class EndCallScreenLogic(QtWidgets.QWidget, Ui_Form):
    def __init__(self, main_window):
        """
        :type main_window: MainWindow.logic.MainWindowLogic
        :param main_window:
        """
        super(EndCallScreenLogic, self).__init__()
        self.setupUi(self)
        self.main_window = main_window
        self.label.setText("""
        <html><head/><body><p><span style=\" font-size:{}px;\">您可以在此提交备注</span></p></body></html>
        """.format(self.main_window.store.config_data.font_size))
        self.pushButton.clicked.connect(self.handle_end_button_clicked)
        self.get_ffmpeg_path()

    def get_ffmpeg_path(self, file=None):
        if file and os.path.basename(file) == 'ffmpeg.exe':
            ffmpeg_path = file
        else:
            work_path = os.path.dirname(sys.argv[0])
            ffmpeg_path = os.path.join(work_path, 'ffmpeg/ffmpeg.exe')
        if os.path.exists(ffmpeg_path):
            self.ffmpeg_path = ffmpeg_path
            self.process()
        else:
            message = QtWidgets.QMessageBox()
            f = message.warning(self, "错误", "未找到ffmpeg文件，点击ok手动指定，或者点击取消退出点名", message.Ok | message.Cancel)
            if f == message.Ok:
                dialog = QtWidgets.QFileDialog()
                file = dialog.getOpenFileName()
                self.get_ffmpeg_path(file[0])
            else:
                self.main_window.close()

    def process(self):
        def handle_success():
            def success():
                if self.pushButton.isEnabled():
                    self.listWidget.addItem("上传完毕,请自行关闭软件")
                else:
                    self.listWidget.addItem("上传成功,软件即将自动关闭")
                    timer = QtCore.QTimer()
                    timer.timeout.connect(lambda: self.main_window.close())
                    timer.start(5000)

            self.listWidget.addItem("音视频资料合并完成,路径为{},大小为{}".format(new_path, os.path.getsize(new_path)))
            self.listWidget.addItem("正在上传文件到服务器")
            response = HttpRequest(
                url='api/upload/call-over-audio/{}/'.format(self.main_window.store.attend_table['id']),
                parent=self.main_window,
                method='post',
                files=new_path
            )
            response.success.connect(lambda: success())
            response.failed.connect(lambda message: self.main_window.warn.add_warn(message, type='error'))
            response.start()

        video_exist = self.main_window.store.device_camera.path and os.path.exists(
            self.main_window.store.device_camera.path)
        audio_exist = self.main_window.store.device_mic.recorder_path and os.path.exists(
            self.main_window.store.device_mic.recorder_path
        )
        if video_exist and audio_exist:
            self.listWidget.addItem("正在合并音视频资料")
            now = datetime.datetime.now()
            new_path = os.path.join(os.getcwd(), "{}-{}-{}-{}-{}-{}.avi".format(
                now.year, now.month, now.day, now.hour, now.minute, now.second
            ))
            # 正常情况
            command = [
                self.ffmpeg_path,
                '-i', self.main_window.store.device_mic.recorder_path,
                '-i', self.main_window.store.device_camera.path,
                '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental',
                new_path
            ]
            f = FFMPEG_THREAD(command, parent=self.main_window)
            f.success.connect(lambda: handle_success())
            f.start()
        elif video_exist and not audio_exist:
            # 仅有视频的情况
            pass
        elif audio_exist and not video_exist:
            # 仅有语音的情况
            pass
        else:
            # 什么都没有的情况
            pass

    def handle_end_button_clicked(self):
        def handle_success():
            self.main_window.warn.add_warn("添加备注成功，您可以离开，文件上传完毕后将会自动关闭")
            self.textEdit.setDisabled(True)
            self.pushButton.setDisabled(True)

        request = HttpRequest(parent=self.main_window, url='api/call_over/call-over-note/', method='post',
                              data={'data': self.textEdit.toPlainText()})
        request.success.connect(lambda data: handle_success())
        request.failed.connect(lambda message: self.main_window.warn.add_warn(message, type='error'))
        request.start()
