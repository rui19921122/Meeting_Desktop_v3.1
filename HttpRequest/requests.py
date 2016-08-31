import json

from PyQt5 import QtCore

import requests
from PyQt5.QtCore import QThread, QMutex
from PyQt5.QtNetwork import QNetworkReply
import pdb
from UrlFunc.url_resolve import parse_url


class HttpRequest(QThread):
    success = QtCore.pyqtSignal(object)
    failed = QtCore.pyqtSignal(str)

    def __init__(self, parent, url: str, method, data=None, files=None):
        super(HttpRequest, self).__init__()
        self.setParent(parent)
        self.method = method
        self.data = data
        self.session = parent.session
        self.url = parse_url(url)
        self.files = files

    def run(self):
        mutex = QMutex()
        mutex.lock()
        try:
            if self.method == 'post':
                if self.files:
                    with open(self.files, 'rb') as file:
                        response = self.session.post(self.url, data=file)
                else:
                    response = self.session.post(self.url, data=self.data)
            elif self.method == 'get':
                response = self.session.get(self.url, data=self.data)
            elif self.method == 'delete':
                response = self.session.delete(self.url, data=self.data)
            else:
                raise Exception('不正确的方法')
            try:
                data = response.json()
            except:
                self.failed.emit("response json解析失败,{}".format(response.text))
                print(response.text)
                return
            if response.status_code >= 300:
                if 'non_field_errors' in data:
                    error_message = data['non_field_errors']
                else:
                    error_message = data.get('error', '未知错误')
                message = '错误,原因为{}'.format(error_message)
                self.failed.emit(message)
            else:
                print(data)
                self.success.emit(data)
        except requests.Timeout as error:
            print('timeout error {}'.format(error))
            self.failed.emit('网络请求错误，超时，请检查网络连接')
        finally:
            mutex.unlock()
            self.deleteLater()
