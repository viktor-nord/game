import pygame
from pytmx.util_pygame import load_pygame
from settings import Settings

class NoTile():
    def __init__(self):
        self.id = -1
        self.collision = 0
        self.exist = True

class Map:
    def __init__(self):
        self.settings = Settings()
        self.size = self.settings.tile_size
        self.tmxdata = Tmx()
        self.removed_tiles = []

    def get_tile(self, x, y, l):
        val = NoTile()
        if len(self.tmxdata.tiles[y][x]["layers"]) == l + 1:
            val = self.tmxdata.tiles[y][x]["layers"][l]
        return val
    
    def is_colliding(self, pos):
        collide = False
        layers = self.tmxdata.tiles[pos[1]][pos[0]]["layers"]
        for layer in layers:
            if layer.collision == 1 and layer.exist == True:
                collide = True
        return collide

    def blit_all_tiles(self, screen):
        for y in self.tmxdata.tiles:
            for x in y:
                for layer in x["layers"]:
                    if layer.exist:
                        img = pygame.transform.scale(layer.image, (self.size, self.size))
                        screen.blit(img, (x["x"], x["y"]))
            
    def change_state(self, pos):
        x = int((pos[0] + self.size / 2) // self.size)
        y = int((pos[1] + self.size / 2) // self.size)
        for i, layer in enumerate(self.tmxdata.tiles[y - 1][x]["layers"]):
            if layer.type == "door":
                self.tmxdata.tiles[y][x]["layers"][i].change_state()

class Tmx:
    def __init__(self):
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
    
    def get_tiles(self):
        tiles = list(range(0, self.y_tiles))
        for y in tiles:
            tiles[y] = list(range(0, self.x_tiles))
            for x in tiles[y]:
                tiles[y][x] = {"x": x * self.size, "y": y * self.size, "layers": []}
        for layer_index, layer in enumerate(self.tmxdata):
            self.layers_amount = layer_index + 1
            for tile in layer.tiles():
                properties = self.try_get_prop(tile, layer_index)
                tile_obj = Tile(tile, layer_index, properties)                
                tiles[tile[1]][tile[0]]["layers"].append(tile_obj)
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
        self.type = properties["type"] 
        self.value = properties["value"] 
        self.width = str(self.size)
        self.height = str(self.size) 
        self.frames = properties["frames"]
        self.exist = True
    
    def change_state(self):
        if self.exist:
            self.exist = False
        else:
            self.exist = True