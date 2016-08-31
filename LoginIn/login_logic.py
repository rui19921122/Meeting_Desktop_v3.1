from HttpRequest import HttpRequest
from Exception.figure_collect_failed import FigureCollectFailed
from DisplayWait.display_wait_logic import DisplayWaitLogic
from .LoginForm import Ui_Form
from PyQt5 import QtWidgets, QtCore, QtGui, QtNetwork
from DataStore import DataStore
from FigureCollect.figure_collect_logic import FigureCollectionLogic


class LoginForm(QtWidgets.QWidget, Ui_Form):
    login_success = QtCore.pyqtSignal()

    def __init__(self, main_window, store, parent):
        """
        :type main_window:MainWindow.logic.MainWindowLogic
        """
        super(LoginForm, self).__init__()
        self.setParent(parent)
        self.main_window = main_window
        self.setupUi(self)
        self.setStyleSheet(r"border-image:url(':/logo/resource/png/bg.jpg')")
        self.LoginButton.setDisabled(True)
        self.FigureButton.setDisabled(True)
        self.LoginButton.clicked.connect(self.handle_login_button_clicked)
        self.FigureButton.clicked.connect(self.handle_figure_button_clicked)
        self.password.textChanged.connect(self.handle_password_change)
        if main_window.store.device_figure.has_device():
            main_window.warn.add_warn("发现指纹仪，您也可以使用指纹仪登陆", type="success")
            self.timer = QtCore.QTimer(self.main_window)
            self.timer.timeout.connect(self.check_figure)
            self.timer.start(1000)
        self.handle_login_button_clicked()

    def check_figure(self):
        self.timer.stop()
        if self.main_window.store.device_figure.pressed():
            try:
                value = self.main_window.store.device_figure.get_figure()
                self.close()
            except FigureCollectFailed:
                self.main_window.warn.add_warn("采集指纹失败", type='error')
                self.timer.start(1000)
                # todo 完善指纹登陆
        else:
            self.timer.start(1000)

    def handle_password_change(self):
        length = len(self.password.text())
        if len(self.password.text()) < 3 or len(self.username.text()) < 3:
            self.LoginButton.setDisabled(True)
            self.FigureButton.setDisabled(True)
        else:
            self.LoginButton.setDisabled(False)
            self.FigureButton.setDisabled(False)

    def handle_login_button_clicked(self):
        thread = HttpRequest(parent=self.main_window, url='api/auth/login/', method='post',
                             data={'username': 'test',
                                   'password': '111111'})
        thread.failed.connect(lambda message: self.main_window.warn.add_warn(message))
        thread.success.connect(lambda: self.handle_login_success())
        thread.start()

    def handle_figure_button_clicked(self):
        thread = HttpRequest(parent=self.main_window, url='api/auth/login/', method='post',
                             data={'username': 'test',
                                   'password': '111111'})
        thread.failed.connect(lambda message: self.main_window.warn.add_warn(message))
        thread.success.connect(lambda: self.handle_login_success(_type='figure'))
        thread.start()

    def handle_login_success(self, _type='login'):
        if _type == 'login':
            display_wait = DisplayWaitLogic(parent=self.main_window.stacked_widget, main_window=self.main_window)
            self.main_window.stacked_layout.addWidget(display_wait)
            self.close()
        elif _type == 'figure':
            display_figure = FigureCollectionLogic(main_window=self.main_window)
            self.main_window.stacked_layout.addWidget(display_figure)
            self.close()

    def handle_reply(self, data):
        print(data)

    def close(self):
        try:
            self.timer.disconnect()
            self.timer.deleteLater()
        except:
            pass
        finally:
            super(LoginForm, self).close()


import logo_rc
