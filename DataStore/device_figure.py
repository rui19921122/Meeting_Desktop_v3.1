import ctypes
from Exception.figure_collect_failed import FigureCollectFailed


class DeviceFigure():
    def __init__(self, main_window):
        """
        :type main_window:MainWindow.logic.MainWindowLogic
        :param main_window:
        """
        self.main_window = main_window
        self.dll = ctypes.windll.LoadLibrary('JZTDevDll.dll')

    def has_device(self):
        _number = self.dll.FPIDevDetect()
        return True if _number == 0 else False

    def get_figure(self, quiet=True):
        '''
        返回指纹模型
        :param quiet: 是否安静模式运行
        :return: 得到的指纹模板
        '''
        # todo 此为阻塞
        pstz = ctypes.create_string_buffer(512)
        length = ctypes.create_string_buffer(512)
        if quiet:
            self.dll.FPIFeatureWithoutUI(0, pstz, length)
        else:
            self.dll.FPIFeature(0, pstz, length)
        if len(pstz.value) == 512:
            return pstz.value.decode('utf-8')
        else:
            raise FigureCollectFailed()

    def pressed(self):
        """
        返回指纹是否按压在指纹仪上
        :return:
        """
        try:
            return True if self.dll.FPICheckFinger(0) == 0 else False
        except:
            self.main_window.warn.add_warn("未发现指纹仪设备")

    def get_figure_template(self):
        '''
        返回指纹特征
        :return:
        '''
        pstz = ctypes.create_string_buffer(512)
        length = ctypes.create_string_buffer(512)
        self.dll.FPITemplate(0, pstz, length)
        if len(pstz.value) == 512:
            pass
        else:
            raise FigureCollectFailed()
        return pstz.value.decode('utf-8')
