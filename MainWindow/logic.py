from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimedia
import logging
from DataStore import DataStore
from Component.PixmapPushButton import PixPushButton
from TitleBar.title_bar_logic import TitleBar
from resource import logo_rc
from LoginIn.login_logic import LoginForm
from Warn.widget import Warning
import requests
from Config.config_dialog import Config


class MainWindowLogic(QtWidgets.QWidget):
    font_size_change = QtCore.pyqtSignal(int)

    def __init__(self, debug=False, logger=None):
        super(MainWindowLogic, self).__init__()
        self.session = requests.session()
        self.logger = logger
        self.debug = debug
        self.store = DataStore(main_window=self)
        self.settings = QtCore.QSettings("WuhuDong", "CallOverSoft")
        font_size = self.settings.value("font-size", "19")
        self.store.config_data.font_size = font_size
        self.central_layout = QtWidgets.QVBoxLayout(self)
        self.stacked_widget = QtWidgets.QWidget()
        self.stacked_layout = QtWidgets.QStackedLayout()
        self.stacked_widget.setLayout(self.stacked_layout)
        self.stacked_layout.setStackingMode(QtWidgets.QStackedLayout.StackAll)
        self.warn = Warning(parent=self.stacked_widget, main_window=self)
        self.stacked_layout.addWidget(self.warn)
        self.set_up_devices()
        self.setup_window()

    def set_up_devices(self):
        '''
        刷新所有设备状态
        :return:
        '''
        setting_mic = self.settings.value("default_mic", None)
        if setting_mic:
            mics = self.store.device_mic.available_mics()
            for i in mics:
                assert isinstance(i, QtMultimedia.QAudioDeviceInfo)
                if i.deviceName() == setting_mic:
                    self.store.device_mic.current_mic = i
        setting_camera = self.settings.value("default_camera", None)
        if setting_mic:
            cameras = self.store.device_camera.available_cameras()
            for i in cameras:
                assert isinstance(i, QtMultimedia.QCameraInfo)
                if i.deviceName() == setting_camera:
                    self.store.device_camera.current_camera = i

    def setup_window(self):
        """
        更改主窗口的样式
        :return:
        """
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.pTitleBar = TitleBar(self, )
        self.installEventFilter(self.pTitleBar)
        self.central_layout.addWidget(self.pTitleBar)
        font_size = self.settings.value('font-size', 1)
        font = QtGui.QFont()
        font.setPointSize(int(font_size))
        self.setFont(font)
        login_form = LoginForm(parent=self.stacked_widget, store=self.store, main_window=self)
        self.stacked_layout.addWidget(login_form)
        self.central_layout.addWidget(self.stacked_widget)
        self.central_layout.setStretch(1, 1)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.central_layout)
        title_timer = QtCore.QTimer(self)  # 更新标题栏用
        title_timer.timeout.connect(lambda: self.pTitleBar.refresh_message())
        title_timer.start(5000)

    def error(self, msg):
        """
        应用内部的logging
        :param msg:
        :return:
        """
        if isinstance(self.logger, logging.Logger) and isinstance(msg, str):
            self.logger.error(msg)

    def show_config(self):
        def setFont(value):
            print(value)
            self.font_size_change.emit(value)
            # font = self.font()
            # font.setPointSize(value)
            # self.setFont(font)

        config = Config(parent=self)
        config.font_change.connect(lambda value: setFont(value))
        config.show()

    def close(self):
        """
        处理应用退出时的状态
        应检测照相机、网络请求、录音笔、视频处理进度
        尤其要注意OpenCV对象的处理
        :return:
        """
        if self.store.device_camera.timer and self.store.device_camera.timer.isActive():
            self.warn.add_warn("正在录制视频，无法退出")
            return
        if self.store.device_mic.recorder and self.store.device_mic.recorder.state() == 1:
            self.warn.add_warn("正在录制音频，无法退出")
            return
        super(MainWindowLogic, self).close()
