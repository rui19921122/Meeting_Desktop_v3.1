from collections import OrderedDict

from .device_mic import DeviceMic
from .device_camera import DeviceCamera
from .device_figure import DeviceFigure
from PyQt5 import QtCore
from .data_config import ConfigData


class DataStore():
    def __init__(self, main_window):
        super(DataStore, self).__init__()
        self.version = '0.1'
        self.device_mic = DeviceMic(main_window=main_window)
        self.device_camera = DeviceCamera(main_window=main_window)
        self.device_figure = DeviceFigure(main_window=main_window)
        self.config_data = ConfigData(main_window=main_window)
        self.attend_table = None
        self.worker_status = OrderedDict()  # 本地维护的出勤人员顺序表
        self.timer_figure = None  # type: QtCore.QTimer
