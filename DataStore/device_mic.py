import os

import datetime
from PyQt5 import QtMultimedia, QtCore


class DeviceMic():
    def __init__(self, main_window):
        self._mic = None
        self.main_window = main_window
        self.recorder = QtMultimedia.QAudioRecorder()  # type:QtMultimedia.QAudioRecorder
        self.recorder_path = None  # type:str
        self.start_time = None
        self.end_time = None

    @property
    def current_mic(self):
        return self._mic

    def start_record(self):
        if self.recorder_path and self.current_mic:
            self.recorder.setAudioInput(
                self.main_window.store.device_mic.current_mic.deviceName())
            settings = QtMultimedia.QAudioEncoderSettings()
            settings.setCodec(r'audio.amr')
            settings.setQuality(QtMultimedia.QMultimedia.HighQuality)
            self.recorder.setEncodingSettings(settings)
            self.main_window.store.device_mic.recorder.setOutputLocation(
                QtCore.QUrl().fromLocalFile(
                    self.recorder_path
                )
            )
            self.main_window.store.device_mic.recorder.record()
            self.main_window.store.device_mic.start_time = datetime.datetime.now()
        else:
            raise EnvironmentError("未设置录音路径或无录音设备")

    def end_record(self):
        if self.recorder.state() == 0:
            return False
        else:
            self.recorder.stop()
            self.end_time = datetime.datetime.now()
            return True

    @current_mic.setter
    def current_mic(self, value):
        if value == self._mic:
            pass
        else:
            self._mic = value
            assert isinstance(self.main_window.settings, QtCore.QSettings)
            self.main_window.settings.setValue("default_mic", value.deviceName())
            self.main_window.settings.sync()

    def available_mics(self):
        """
        """
        info = QtMultimedia.QAudioDeviceInfo()
        return info.availableDevices(QtMultimedia.QAudio.AudioInput)
