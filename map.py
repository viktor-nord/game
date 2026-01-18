import pygame
from pytmx.util_pygame import load_pygame
from settings import Settings

class NoTile():
    def __init__(self):
        self.id = -1
        self.collision = 0
        self.type = "none"
        self.exist = False
    
class Map:
    def __init__(self):
        self.settings = Settings()
        self.size = self.settings.tile_size
        self.removed_tiles = []
        self.tmxdata = load_pygame('map/example_maptmx.tmx')
        self.settings = Settings()
        self.y_tiles = self.settings.y_tiles
        self.x_tiles = self.settings.x_tiles
        self.screen_width = self.settings.screen_width
        self.screen_height = self.settings.screen_height
        self.size = self.settings.tile_size
        self.layers_amount = 0
        self.tiles = self.get_tiles()
        self.base_tile_prop = {
            'id': -1, 
            'animation': 0, 
            'collision': 0, 
            'is_overlay': 0, 
            'type': '', 
            'value': '', 
            'width': str(self.size), 
            'height': str(self.size), 
            'frames': [],
            'exist': True
        }


    def is_colliding(self, pos):
        collide = False
        layers = self.tiles[pos[1]][pos[0]]
        for layer in layers:
            if layer.collision == 1 and layer.exist == True:
                collide = True
        return collide

    def blit_all_tiles(self, screen):
        for yi, y in enumerate(self.tiles):
            for xi, x in enumerate(y):
                for tile in x:
                    if tile.exist:
                        screen.blit(tile.image, (xi * self.size, yi * self.size))
            
    def change_state(self, player):
        x = int((player.rect.x + self.size / 2) // self.size)
        y = int((player.rect.y + self.size / 2) // self.size)
        print(player.dir)
        if player.dir == "up":
            y -= 1
        if player.dir == "down":
            y += 1
        if player.dir == "right":
            x += 1
        if player.dir == "left":
            x -= 1
        for i, tile in enumerate(self.tiles[y][x]):
            if tile.type == "door" and tile.id > 0:
                self.tiles[y][x][i].change_state()
    
    def get_tiles(self):
        tiles = list(range(0, self.y_tiles))
        for y in tiles:
            tiles[y] = list(range(0, self.x_tiles))
            for x in tiles[y]:
                tiles[y][x] = []
                for layer in enumerate(self.tmxdata):
                    tiles[y][x].append(NoTile())
        for layer_index, layer in enumerate(self.tmxdata):
            self.layers_amount = layer_index + 1
            for tile in layer.tiles():
                properties = self.try_get_prop(tile, layer_index)
                tile_obj = Tile(tile, layer_index, properties)                
                tiles[tile[1]][tile[0]][layer_index] = tile_obj
        return tiles
    
    def try_get_prop(self, tile, layer):
        try:
            properties = self.tmxdata.get_tile_properties(tile[0], tile[1], layer)
        except ValueError:
            properties = self.base_tile_prop
        if properties is None:
            properties = self.base_tile_prop
        return properties

class Tile:
    def __init__(self, tmx_tile, layer_index, properties):
        self.tmx_tile = tmx_tile
        self.size = Settings().tile_size
        self.x = tmx_tile[0]
        self.y = tmx_tile[1]
        self.image = pygame.transform.scale(tmx_tile[2], (self.size, self.size))
        self.layer = layer_index
        properties = properties
        self.id = properties["id"]
        self.animation = properties["animation"]
        self.collision = properties["collision"]
        self.is_overlay = properties["is_overlay"]
        # Types: 'chest', 'summon', 'wall', 'door', 'object', 'ground'
        self.type = properties["type"] 
        self.value = properties["value"] 
        self.width = str(self.size)
        self.height = str(self.size) 
        self.frames = properties["frames"]
        self.exist = True
    
    def change_state(self):
        print("ee")
        if self.exist:
            self.exist = False
        else:
            self.exist = True