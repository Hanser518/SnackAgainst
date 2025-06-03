
class Params:
    def __init__(self):
        self.window_model = 0
        self.window_list = [(1280, 720),  (1920, 1080), (2560, 1440)]

        self.MATRIX_SIZE = (40, 20)
        self.WINDOW_MIN = 0
        self.WINDOW_MEDIUM = 1
        self.WINDOW_MAX = 2

    def set_window_model(self, window_model):
        self.window_model = window_model

    def get_window_size(self):
        return self.window_list[self.window_model]

    def get_matrix_size(self):
        return self.MATRIX_SIZE