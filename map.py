import pygame
from pytmx.util_pygame import load_pygame
from settings import Settings

# collision
# 2 = right
# 3 = bottom right
# 4 = bottom
# 5 = bottom left
# 6 = left
# 7 = top left
# 8 = top
# 9 = top right

class NoTile():
    def __init__(self):
        self.id = -1
        self.collision = 0
        self.exist = False

class Map:
    def __init__(self, id='map_1'):
        base_url = 'assets/maps/'
        src = f"{base_url}{id}.tmx"
        self.settings = Settings()
        self.size = self.settings.tile_size
        self.removed_tiles = []
        self.collision_grid = []
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
        self.mobile_collision_grid = {}
        self.tmxdata = load_pygame(src)
        self.tiles = self.get_tile_grid()

    def get_tile(self, x, y, l):
        val = NoTile()
        if len(self.tiles[y][x]["layers"]) == l + 1:
            val = self.tiles[y][x]["layers"][l]
        return val

    def get_tile_layers(self, x, y):
        val = []
        for tile in self.tiles[y][x]["layers"]:
            val.append(tile)                
        return val

    def get_tile_collision(self, x, y):
        val = None
        if all(x.id < 0 for x in self.get_tile_layers(x, y)):
            return 1
        for pos in self.mobile_collision_grid.values():
            if pos[0] == x and pos[1] == y:
                return 1
        for tile in self.collision_grid:
            if tile['x'] == x and tile['y'] == y:
                return tile['type']
        return val

    def check_collision(self, character):
        posible_moves = {
            'right': self.not_colliding('right', character),
            'left': self.not_colliding('left', character),
            'down': self.not_colliding('down', character),  
            'up': self.not_colliding('up', character)
        }
        return posible_moves

    def not_colliding(self, dir, character):
        not_colliding = True
        r = pygame.Rect(
            (character.rect.x + 4, character.rect.y + 4), 
            (character.rect.width - 8, character.rect.height - 8)
        )
        r.x += character.movement[dir][0] * character.speed
        r.y += character.movement[dir][1] * character.speed
        max_vertical = len(self.tiles[r.y // self.size]) < r.right / self.size
        max_horisontal = len(self.tiles) < r.bottom / self.size
        # screen border
        if r.x < 0 or r.y < 0 or max_horisontal or max_vertical:
            return False
        # npc
        for npc_id, npc in self.mobile_collision_grid.items():
            if npc_id != character.id:
                npc_rect = pygame.Rect(
                    (npc[0] * self.size + 2, npc[1] * self.size + 2), 
                    (self.size - 4, self.size - 4)
                )
                if r.colliderect(npc_rect):
                    not_colliding = False
        # tiles
        for col_obj in self.collision_grid:
            rect_arr = self.get_collision_box_arr(col_obj['x'] * self.size, col_obj['y'] * self.size, col_obj['type'])
            for rect in rect_arr:
                if r.colliderect(rect):
                    if col_obj['type'] == 10:
                        return True
                    else:
                        not_colliding = False
        return not_colliding

    def x_y_w_h(self, x_pos, y_pos, count, type):
        x = x_pos
        y = y_pos
        w = 1
        h = 1
        if type == 1 or type == 10:
            w = 32
            h = 32
        elif type == 2:
            x = x_pos + 31
            h = 32
        elif type == 3:
            x = x_pos + 31 - count
            y = y_pos + count
            w = 1 + count
        elif type == 4:
            y = y_pos + 31
            w = 32
        elif type == 5:
            y = y_pos + count
            w = 1 + count
        elif type == 6:
            h = 32
        elif type == 7:
            y = y_pos + count
            w = 32 - count
        elif type == 8:
            w = 32
        elif type == 9:
            x = x_pos + count
            y = y_pos + count
            w = 32 - count
        return x, y, w, h

    def get_collision_box_arr(self, x_pos, y_pos, type):
        arr = []
        count = 0
        if type == 1 or type == 2 or type == 4 or type == 6 or type == 8 or type == 10:
            count = 31
        while count < 32:
            x, y, w, h = self.x_y_w_h(x_pos, y_pos, count, type)
            r = pygame.Rect((x, y), (w, h))
            arr.append(r)
            count += 1
        return arr

    def blit_all_tiles(self, screen):
        # return
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
                    tile_x = self.tiles[pos[1]][pos[0]]["x"]
                    tile_y = self.tiles[pos[1]][pos[0]]["y"]
                    self.blit_tile(tile, tile_x, tile_y, screen)
    
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
        tiles = self.get_sceleton_grid()
        for layer_index, layer in enumerate(self.tmxdata):
            self.layers_amount = layer_index + 1
            for tile in layer.tiles():
                properties = self.try_get_prop(tile, layer_index)
                if properties['collision'] > 0:
                    self.set_collision_grid(tile, properties)
                properties["frame_images"] = self.get_animation_frames(properties["frames"])
                tile_obj = Tile(tile, layer_index, properties)                
                tiles[tile[1]][tile[0]]["layers"].append(tile_obj)
        return tiles
    
    def get_sceleton_grid(self):
        tiles = list(range(0, self.settings.y_tiles))
        for y in tiles[:]:
            tiles[y] = list(range(0, self.settings.x_tiles))
            for x in tiles[y]:
                tiles[y][x] = {"x": x * self.size, "y": y * self.size, "layers": []}
        return tiles

    def set_collision_grid(self, tile, properties):
        for col in self.collision_grid:
            if col['x'] == tile[0] and col['y'] == tile[1]:
                self.collision_grid.remove(col)
        collision_obj = {'x': tile[0], 'y': tile[1], 'type': properties['collision']}
        self.collision_grid.append(collision_obj)

    def get_animation_frames(self, frames):
        arr = []
        for frame in frames:
            img = self.tmxdata.get_tile_image_by_gid(frame.gid)
            arr.append(img)
        return arr

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
