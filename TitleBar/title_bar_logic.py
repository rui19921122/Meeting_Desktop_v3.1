from PyQt5 import QtWidgets, QtCore, QtGui


class TitleBar(QtWidgets.QWidget):
    def __init__(self, parent):
        '''
        :type parent: MainWindow.logic.MainWindowLogic
        :param parent:
        '''
        super(TitleBar, self).__init__(parent)
        self.setFixedHeight(30)
        self.main_window = parent
        self.m_status_label = QtWidgets.QLabel(self)
        self.m_status_label.setText("上海铁路局芜湖东站点名会系统")
        self.m_pTitleLabel = QtWidgets.QLabel(self)
        m_pMinimizeButton = QtWidgets.QPushButton(self)
        m_pCloseButton = QtWidgets.QPushButton(self)

        # self.m_status_label.setFixedSize(30, 30)
        self.m_status_label.setScaledContents(True)

        self.m_pTitleLabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                         QtWidgets.QSizePolicy.Fixed)

        m_pMinimizeButton.setFixedSize(30, 30)
        m_pMinimizeButton.setIcon(QtGui.QIcon(":/logo/png/min.png"))
        m_pMinimizeButton.setIconSize(QtCore.QSize(30, 30))
        m_pMinimizeButton.clicked.connect(lambda: parent.showMinimized())
        m_pCloseButton.setFixedSize(30, 30)
        m_pCloseButton.setIcon(QtGui.QIcon(":/logo/png/close.png"))
        m_pCloseButton.setIconSize(QtCore.QSize(30, 30))
        m_pCloseButton.clicked.connect(lambda: parent.close())

        self.m_pTitleLabel.setObjectName("whiteLabel")
        m_pCloseButton.setObjectName("closeButton")
        config_button = QtWidgets.QPushButton()
        config_button.setFixedSize(30, 30)
        config_button.setIcon(QtGui.QIcon(":/logo/resource/png/config.png"))
        config_button.setIconSize(QtCore.QSize(30, 30))
        config_button.clicked.connect(parent.show_config)

        config_button.setToolTip("设置")
        m_pMinimizeButton.setToolTip("最小化")
        m_pCloseButton.setToolTip("关闭")

        pLayout = QtWidgets.QHBoxLayout(self)
        pLayout.addWidget(self.m_status_label)
        pLayout.addSpacing(5)
        pLayout.addWidget(self.m_pTitleLabel)
        pLayout.addWidget(config_button)
        pLayout.addWidget(m_pMinimizeButton)
        pLayout.addWidget(m_pCloseButton)
        pLayout.setSpacing(0)
        pLayout.setContentsMargins(5, 0, 5, 0)
        self.setLayout(pLayout)

    def set_message(self, message):
        self.m_pTitleLabel.setText("上海铁路局芜湖东站点名会系统 " + message)

    def refresh_message(self):
        record_audio = True if self.main_window.store.device_mic.recorder.state() == 1 else False
        record_video = True if self.main_window.store.device_camera.capturing else False
        if record_audio and record_video:
            message = "---正在录音和录像"
        elif record_audio and not record_video:
            message = "---正在录音"
        elif not record_audio and record_video:
            message = '---正在录像'
        else:
            message = ''
        self.m_status_label.setText("上海铁路局芜湖东站点名会系统 " + message)
