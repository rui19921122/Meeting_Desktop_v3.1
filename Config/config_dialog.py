from PyQt5 import QtGui, QtCore, Qt, QtWidgets, QtMultimedia
from .ConfigForm import Ui_Dialog


class Config(QtWidgets.QDialog, Ui_Dialog):
    font_change = QtCore.pyqtSignal(int)

    def __init__(self, parent):
        """
        :type parent: MainWindow.logic.MainWindowLogic
        """
        super(Config, self).__init__(parent)
        self._parent = parent
        self.setFont(parent.font())
        self.setupUi(self)
        self.font_spin_box.setValue(int(parent.store.config_data.font_size))
        self.SubmitButton.clicked.connect(self.on_submit)
        self.ResetButton.clicked.connect(lambda: self.close())
        mics = parent.store.device_mic.available_mics()
        if len(mics) > 0:
            self.micBox.addItems(map(lambda value: value.deviceName(), mics))
            if parent.store.device_mic.current_mic:
                self.micBox.setCurrentIndex(mics.index(parent.store.device_mic.current_mic))
        else:
            self.micBox.addItem("未发现设备")
            self.micBox.setDisabled(True)
        cameras = parent.store.device_camera.available_cameras()
        if len(cameras) > 0:
            self.cameraBox.addItems(map(lambda value: value.deviceName(), cameras))
            if parent.store.device_camera.current_camera:
                self.cameraBox.setCurrentIndex(cameras.index(parent.store.device_camera.current_camera))
        else:
            self.cameraBox.addItem("未发现设备")
            self.cameraBox.setDisabled(True)
        self.figureBox.addItem("有指纹仪" if parent.store.device_figure.has_device() else "无指纹仪")
        self.figureBox.setDisabled(True)

    def on_submit(self):
        self._parent.store.config_data.font_size = self.font_spin_box.value()
        self.font_change.emit(self.font_spin_box.value())
        if self.cameraBox.isEnabled():
            name = self.cameraBox.itemText(self.cameraBox.currentIndex())
            for camera in self._parent.store.device_camera.available_cameras():
                if camera.deviceName() == name:
                    self._parent.store.device_camera.current_camera = camera
        if self.micBox.isEnabled():
            name = self.micBox.itemText(self.micBox.currentIndex())
            for mic in self._parent.store.device_mic.available_mics():
                if mic.deviceName() == name:
                    self._parent.store.device_mic.current_mic = mic
        self.close()