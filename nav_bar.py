import pygame

class NavBar:
    def __init__(self):
        self.pages = ["general", "religion", "race", "ability", "miracles", "submit"]
        self.available_pages = ["general", "religion", "race", "ability", "miracles", "submit"]
        pos_x = 836
        pos_y = 82
        self.current = self.pages[0]
        self.base_rect = pygame.Rect((pos_x, pos_y), (46, 32))
        width = 46
        height = 32 + 50 * (len(self.pages) - 1)
        self.surf = pygame.Surface((width, height), pygame.SRCALPHA)
        self.list = self.get_list(self.available_pages, self.base_rect)
        self.render_list()
        self.rect = self.surf.get_rect(x = pos_x, y = pos_y)

    def get_list(self, pages, rect):
        arr = []
        for i, text in enumerate(pages):
            arr.append(NavItem(i + 1, text, rect.move(0, 50 * i)))
        return arr

    # def update_nav(self, completed_amount):
    #     for i, page in enumerate(self.pages):
    #         if i < completed_amount + 1:
    #             if page not in self.available_pages:
    #                 self.available_pages.append(page)
    #     self.list = self.get_list(self.available_pages, self.base_rect)
    #     self.render_list()

    def render_list(self):
        for i, item in enumerate(self.list):
            self.surf.blit(item.surf, (0, 50 * i))

    def handle_click(self):
        mouse_pos = pygame.mouse.get_pos()
        for item in self.list:
            if item.rect.collidepoint(mouse_pos):
                self.current = item.value

    def blitme(self, screen):
        screen.blit(self.surf, self.rect)

class NavItem:
    def __init__(self, icon, value, rect):
        self.id = icon
        self.value = value
        self.img = pygame.image.load("assets/ui_sprites/Sprites/Content/5 Holders/nav_item.png").convert_alpha()
        self.surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        self.rect = rect
        self.surf.blit(self.img, (0,0))
        self.icon_img = pygame.image.load(f"assets/ui_sprites/Sprites/Content/1 Items/{icon}.png").convert_alpha()
        self.icon_rect = self.icon_img.get_rect(center = self.surf.get_rect().center)
        self.surf.blit(self.icon_img, self.icon_rect)
