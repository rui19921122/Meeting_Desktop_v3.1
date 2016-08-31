from PyQt5 import QtCore

from PyQt5 import QtMultimedia

try:
    import cv2
except:
    raise ImportError("导入cv2模块出错")


class DeviceCamera():
    def __init__(self, main_window, fps=8, port=0):
        self._camera = None
        self.main_window = main_window
        self.path = None
        self.capturing = False
        self.fps = fps
        self.timer = QtCore.QTimer(self.main_window)
        self.sec = 1000 / self.fps
        self.port = port
        self.cap = None
        self.out = None

    @property
    def current_camera(self):
        return self._camera

    @current_camera.setter
    def current_camera(self, value):
        if value == self._camera:
            pass
        else:
            self._camera = value
            self.main_window.settings.setValue("default_camera", value.deviceName())
            self.main_window.settings.sync()

    def available_cameras(self):
        return QtMultimedia.QCameraInfo().availableCameras()

    def start_capture(self):
        if self.path:
            self.cap = cv2.VideoCapture(self.port)
            self._fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.out = cv2.VideoWriter(self.path, self._fourcc, self.fps, (640, 480))
            self.capturing = True
            self.timer.timeout.connect(self.nextFrameSlot)
            self.timer.start(self.sec)
        else:
            raise ValueError("未设置保存路径")

    def nextFrameSlot(self):
        ret, frame = self.cap.read()
        if ret == True and self.capturing and self.cap.isOpened():
            frame = cv2.flip(frame, 0)
            # write the flipped frame
            self.out.write(frame)
            # cv2.imshow('frame', frame)
        else:
            # 失败清理
            self.path = None
            self.capturing = False
            self.timer.stop()
            self.timer.disconnect()
            self.main_window.warn.add_warn("摄像失败", type='error')
            self.cap.release()
            self.out.release()

    def end_capture(self):
        self.capturing = False
        self.timer.stop()
        self.cap.release()
        self.out.release()
