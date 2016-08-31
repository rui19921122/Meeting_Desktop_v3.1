class FigureCollectFailed(BaseException):
    def __init__(self, *args, **kwargs):
        super(FigureCollectFailed, self).__init__(*args, **kwargs)
