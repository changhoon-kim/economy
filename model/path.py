import os

class Path:
    def __init__(self):
        self.data = os.path.abspath(os.path.join(__file__, '..', '..', 'datas'))
        self.report = os.path.abspath(os.path.join(__file__, '..', '..', 'reports'))
