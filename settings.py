class Settings():
    def __init__(self):
        self.tile_size = 32
        self.x_tiles = 32
        self.y_tiles = 16
        self.screen_width = self.x_tiles * self.tile_size # 1024
        self.screen_height = self.y_tiles * self.tile_size # 512
