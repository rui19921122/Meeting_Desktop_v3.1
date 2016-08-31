# -*- coding: utf-8 -*-
import sys
import os
import traceback
import logging
import logging.handlers
from MainWindow.logic import MainWindowLogic

sys.path.append(os.path.abspath('..'))

import requests
from PyQt5 import QtWidgets, QtCore, QtGui, QtWebKitWidgets

from logging import Logger


def handle_exception(exc_type, exc_value, exc_traceback):
    """ handle all exceptions """

    ## KeyboardInterrupt is a special case.
    ## We don't raise the error dialog when it occurs.
    if issubclass(exc_type, KeyboardInterrupt):
        if QtWidgets.QApplication:
            QtWidgets.QApplication.quit()
        return
    if issubclass(exc_type, KeyboardInterrupt):
        if QtGui.qApp:
            QtGui.qApp.quit()
        return

    filename, line, dummy, dummy = traceback.extract_tb(exc_traceback).pop()
    filename = os.path.basename(filename)
    error = "%s: %s" % (exc_type.__name__, exc_value)
    logger.debug(error)
    # QtWidgets.QMessageBox.critical(None, "Error",
    #                                r'''A critical error has occured,{},
    #                                It occurred at line {} of file {}
    #                                '''.format(error, line, filename))

    print("Closed due to an error. This is the full error report:")
    print('')
    print("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
    sys.exit(1)


sys.excepthook = handle_exception
if __name__ == '__main__':
    LOG_FILE = 'tst.log'
    sys.path.append(os.getcwd())
    handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)
    fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
    formatter = logging.Formatter(fmt)  # 实例化formatter
    handler.setFormatter(formatter)  # 为handler添加formatter
    logger = logging.getLogger('tst')  # 获取名为tst的logger
    logger.addHandler(handler)  # 为logger添加handler
    logger.setLevel(logging.DEBUG)
    app = QtWidgets.QApplication(sys.argv)
    qss = open('./OSXLite.qss').read()
    app.setStyleSheet(qss)
    # todo 完成翻译工作
    # trans = QtCore.QTranslator()
    # ok = trans.load(r"qt_zh_CN.qm")
    # app.installTranslator(trans)
    mainWindow = MainWindowLogic(logger=logger, debug=True)
    mainWindow.showMaximized()
    sys.exit(app.exec_())
