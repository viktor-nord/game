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
        # self.tmxdata = Tmx()
        self.removed_tiles = []
        self.layers_amount = 0
        self.base_tile_prop = {
            'id': -1, 
            'collision': 0, 
            'is_overlay': 0, 
            'type': '', 
            'value': '', 
            'width': str(self.size), 
            'height': str(self.size), 
            'frames': [],
            'exist': True,
            'frame_images': []
        }
        self.tmxdata = load_pygame('map/fan_tasy_1.tmx')
        self.tiles = self.get_tile_grid()

    def get_tile(self, x, y, l):
        val = NoTile()
        if len(self.tiles[y][x]["layers"]) == l + 1:
            val = self.tiles[y][x]["layers"][l]
        return val
    
    def check_collision(self, player_rect):
        not_colliding = True
        return not_colliding

    def is_colliding(self, pos):
        collide = False
        if pos[0] < 0 or pos[1] < 0 or len(self.tiles) == pos[1] or len(self.tiles[pos[1]]) == pos[0]:
            return True
        for layer in self.tiles[pos[1]][pos[0]]["layers"]:
            if layer.collision == 1 and layer.exist == True:
                collide = True
        return collide

    def blit_all_tiles(self, screen):
        for y in self.tiles:
            for x in y:
                for tile in x["layers"]:
                    if tile.exist:
                        self.blit_tile(tile, x["x"], x["y"], screen)
                        tile.update_frame_counter()
    
    def blit_overlay(self, player_rect, screen):
        x = int((player_rect.x + self.size / 2) // self.size)
        y = int((player_rect.y + self.size / 2) // self.size)
        positions = [
            (x, y),
            (x, y + 1),
            (x + 1, y),
            (x + 1, y + 1),
            (x - 1, y),
            (x - 1, y + 1)
        ]
        for p in positions[:]:
            if self.tile_does_not_exist(p[0], p[1]):
                positions.remove(p)
        for pos in positions:
            for tile in self.tiles[pos[1]][pos[0]]["layers"]:
                if tile.is_overlay:
                    self.blit_tile(tile, self.tiles[pos[1]][pos[0]]["x"], self.tiles[pos[1]][pos[0]]["y"], screen)
    
    def tile_does_not_exist(self, x, y):
        if x < 0 or y < 0 or len(self.tiles) == y or len(self.tiles[y]) == x:
            return True
        else:
            return False

    def blit_tile(self, tile, x, y, screen):
        img = tile.image
        if len(tile.frame_images) > 0:
            img = tile.frame_images[tile.frame_index]
        transformed_image = pygame.transform.scale(img, (self.size, self.size))
        screen.blit(transformed_image, (x, y))

    def change_state(self, pos):
        x = int((pos[0] + self.size / 2) // self.size)
        y = int((pos[1] + self.size / 2) // self.size)
        for i, layer in enumerate(self.tiles[y - 1][x]["layers"]):
            if layer.type == "door":
                self.tiles[y][x]["layers"][i].change_state()

    def get_tile_grid(self):
        tiles = list(range(0, self.settings.y_tiles))
        for y in tiles:
            tiles[y] = list(range(0, self.settings.x_tiles))
            for x in tiles[y]:
                tiles[y][x] = {"x": x * self.size, "y": y * self.size, "layers": []}
                # for layer in enumerate(self.tmxdata):
                #     tiles[y][x].append(NoTile())
        for layer_index, layer in enumerate(self.tmxdata):
            self.layers_amount = layer_index + 1
            for tile in layer.tiles():
                properties = self.try_get_prop(tile, layer_index)
                properties["frame_images"] = []
                for frame in properties["frames"]:
                    img = self.tmxdata.get_tile_image_by_gid(frame.gid)
                    properties["frame_images"].append(img)
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
        self.collision = properties["collision"]
        self.is_overlay = properties["is_overlay"]
        # Types: 'chest', 'summon', 'wall', 'door', 'object', 'ground'
        self.type = properties["type"] 
        self.value = properties["value"] 
        self.width = str(self.size)
        self.height = str(self.size) 
        self.frames = properties["frames"]
        self.frame_images = properties["frame_images"]
        self.frame_counter = 0
        self.frame_index = 0
        self.exist = True
    
    def change_state(self):
        if self.exist:
            self.exist = False
        else:
            self.exist = True

    def update_frame_counter(self):
        self.frame_counter += 1
        if self.frame_counter > 10:
            self.frame_counter = 0
            self.frame_index += 1
        if self.frame_index >= len(self.frame_images):
            self.frame_index = 0 
