import pygame

class Settings():
    def __init__(self):
        self.tile_size = 32
        self.x_tiles = 32
        self.y_tiles = 16
        self.fps = 60
        self.screen_width = self.x_tiles * self.tile_size # 1024
        self.screen_height = self.y_tiles * self.tile_size # 512
        self.center = (self.screen_width / 2, self.screen_height / 2)
        self.text_color = (13, 141, 103) # hex 0d8d67
        self.color_active = (110, 197, 49) # hex 6ec531
        self.color_red = (201, 37, 25) # hex C92519
        self.color_silver = (217, 218, 219)
        self.special_keys = special_keys
        self.letter_keys = letter_keys
        self.number_keys = number_keys
        self.permitted_keys = self.get_permitted_keys()

    def get_permitted_keys(self):
        arr = []
        for key in self.special_keys:
            arr.append(key)
        for key in self.letter_keys:
            arr.append(key)
        for key in self.number_keys:
            arr.append(key)
        return arr


special_keys = [
    pygame.K_BACKSPACE,
    pygame.K_SPACE,
    pygame.K_RETURN,
    pygame.K_LEFT,
    pygame.K_RIGHT,
]
letter_keys = [
    pygame.K_q,
    pygame.K_w,
    pygame.K_e,
    pygame.K_r,
    pygame.K_t,
    pygame.K_y,
    pygame.K_u,
    pygame.K_i,
    pygame.K_o,
    pygame.K_p,
    pygame.K_a,
    pygame.K_s,
    pygame.K_d,
    pygame.K_f,
    pygame.K_g,
    pygame.K_h,
    pygame.K_j,
    pygame.K_k,
    pygame.K_l,
    pygame.K_z,
    pygame.K_x,
    pygame.K_c,
    pygame.K_v,
    pygame.K_b,
    pygame.K_n,
    pygame.K_m,
]
number_keys = [
    pygame.K_0,
    pygame.K_1,
    pygame.K_2,
    pygame.K_3,
    pygame.K_4,
    pygame.K_5,
    pygame.K_6,
    pygame.K_7,
    pygame.K_8,
    pygame.K_9,
]
