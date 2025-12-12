from email.mime import image
from turtle import width
import pygame as py
from font import Text

class TextBox:
    def __init__(self, game, text, parent, title=""):
        self.game = game
        self.parent = parent
        self.title = title
        self.width = parent.width - 32
        self.src = py.image.load("assets/ui_sprites/SpriteSheet/Folding & Cutout Paper UI SpriteSheet.png")
        self.size = (32,32)
        self.text_container = py.Rect((4, 4), (parent.width - 32 - 8, 10))
        self.text = Text(text, self.text_container, has_underline=True, centered=False)
        self.image = py.Surface((self.width, self.text.rect.height), py.SRCALPHA)
        self.rect = self.image.get_rect(x=parent.x + 16, y=parent.y)
        self.images = self.get_box()
        self.render_box()
        self.image.blit(self.text.image, self.text.rect)

    def render_box(self):
        h = self.text.rect.height
        # height = self.rect.height // 16
        height = h // 16
        width = self.width // 16
        for y in range(0, height):
            for x in range(0, width):
                # print(f"y: {y}, x: {x}")
                img = self.images["blank"]
                if y == 0 and x == 0:
                    img = self.images["top_left"]
                elif y == height - 1 and x == 0:
                    img = self.images["bottom_left"]
                elif y == 0 and x == width - 1:
                    img = self.images["top_right"]
                elif y == height - 1 and x == width - 1:
                    img = self.images["bottom_right"]
                elif y > 0 and x == 0:
                    img = self.images["left"]
                elif y == 0 and x > 0:
                    img = self.images["top"]
                elif y > 0 and x == width - 1:
                    img = self.images["right"]
                elif y == height - 1 and x > 0:
                    img = self.images["bottom"]
                self.image.blit(img, (x*16, y*16))
        # self.image.blit(self.images["top_left"], (0,0))


    def get_box(self):
        x = -448
        y = -3856
        size = (16,16)
        top_left = py.Surface(size, py.SRCALPHA)
        top_left.blit(self.src, (x, y))
        top_right = py.transform.flip(top_left, True, False)
        bottom_left = py.transform.flip(top_left, False, True)
        bottom_right = py.transform.flip(top_left, True, True)
        top = py.Surface(size, py.SRCALPHA)
        top.blit(self.src, (x - 8, y))
        bottom = py.transform.flip(top, False, True)
        left = py.Surface(size, py.SRCALPHA)
        left.blit(self.src, (x, y - 6))
        right = py.transform.flip(left, True, False)
        blank = py.Surface(size, py.SRCALPHA)
        blank.blit(self.src, (x - 8, y - 8))
        dic = {
            "top_left": top_left,
            "top": top,
            "top_right": top_right,
            "left": left,
            "right": right,
            "bottom_left": bottom_left,
            "bottom": bottom,
            "bottom_right": bottom_right,
            "blank": blank
        }
        return dic
    


    # def get_small_container(self, type=1):
    #     x = -2790
    #     y = -3654 if type == 1 else -3766
    #     top_left = py.Surface(self.size, py.SRCALPHA)
    #     top_left.blit(self.src, (x, y))
    #     top = py.Surface(self.size, py.SRCALPHA)
    #     top.blit(self.src, (x - 32, y))
    #     top_right = py.Surface(self.size, py.SRCALPHA)
    #     top_right.blit(self.src, (x - 64, y))
    #     left = py.Surface(self.size, py.SRCALPHA)
    #     left.blit(self.src, (x, y - 32))
    #     right = py.Surface(self.size, py.SRCALPHA)
    #     right.blit(self.src, (x - 64, y - 32))
    #     bottom_left = py.Surface(self.size, py.SRCALPHA)
    #     bottom_left.blit(self.src, (x, y - 64))
    #     bottom = py.Surface(self.size, py.SRCALPHA)
    #     bottom.blit(self.src, (x - 32, y - 64))
    #     bottom_right = py.Surface(self.size, py.SRCALPHA)
    #     bottom_right.blit(self.src, (x - 64, y - 64))
    #     dic = {
    #         "top_left": top_left,
    #         "top": top,
    #         "top_right": top_right,
    #         "left": left,
    #         "right": right,
    #         "bottom_left": bottom_left,
    #         "bottom": bottom,
    #         "bottom_right": bottom_right,
    #     }
    #     return dic

    def blitme(self):
        self.game.screen.blit(self.image, self.rect)
        # py.draw.rect(self.game.screen, "red", self.image.get_rect(y = self.rect.y, x = self.rect.x + 4 , width = self.image.get_width() - 8, height=50))
        # self.game.screen.blit(self.images["top_left"], (0,0))
        # self.game.screen.blit(self.images["top"], (16,0))
        # self.game.screen.blit(self.images["top_right"], (32,0))
        # self.game.screen.blit(self.images["left"], (0,16))
        # self.game.screen.blit(self.images["right"], (32,16))
        # self.game.screen.blit(self.images["bottom_left"], (0,32))
        # self.game.screen.blit(self.images["bottom"], (16,32))
        # self.game.screen.blit(self.images["bottom_right"], (32,32))
        # self.game.screen.blit(self.images["blank"], (16,16))
        