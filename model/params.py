class Params:
    def __init__(self):
        self.window_model = 0
        self.window_list = [(1280, 720), (1920, 1080), (2560, 1440)]

        self.MATRIX_SIZE = (60, 30)
        self.BLOCK_SIZE = 0
        self.WINDOW_MIN = 0
        self.WINDOW_MEDIUM = 1
        self.WINDOW_MAX = 2
        self.INFO_HEIGHT = 0
        self.INFO_WIDTH = 0

        self.update_block_info()

    def set_window_model(self, window_model):
        self.window_model = window_model
        self.update_block_info()

    def get_window_size(self):
        return self.window_list[self.window_model]

    def get_matrix_size(self):
        return self.MATRIX_SIZE

    def update_block_info(self):
        self.BLOCK_SIZE = self.window_list[self.window_model][0] // self.MATRIX_SIZE[0]
        self.INFO_HEIGHT = self.BLOCK_SIZE * self.MATRIX_SIZE[1]
        self.INFO_WIDTH = self.BLOCK_SIZE * self.MATRIX_SIZE[0]
