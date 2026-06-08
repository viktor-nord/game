import pygame
from pytmx import pytmx
from pytmx.util_pygame import load_pygame
from settings import Settings

size = Settings().tile_size

class Map3:
    def __init__(self, id='map_1'):
        src = "assets/maps/test_col_n_obj.tmx"
        self.removed_tiles = []
        self.collision_grid = []
        self.layers_amount = 0
        self.mobile_collision_grid = {}
        self.offset = [0,0]
        self.tmxdata = load_pygame(src, pixelalpha=True)
        self.tiles, self.objects, self.colliders = self.get_tile_grid()
        self.add_world_border()

    def add_world_border(self):
        w, h = (self.tmxdata.width * size) / 2, (self.tmxdata.height * size) / 2
        colliders = {
            "left_border": pygame.Rect((-10, -10), (10, h + 20)),
            "right_border": pygame.Rect((w + 32, -10), (10, h + 20)),
            "up_border": pygame.Rect((-10, -10), (w + 20, 10)),
            "down_border": pygame.Rect((-10, h - 64), (w + 40, 10))
        }
        for key, val in colliders.items():
            self.colliders.append(Collider(val, key))

    def get_tile_layers(self, x, y):
        val = []
        for tile in self.tiles[y][x]["layers"]:
            val.append(tile)                
        return val

    def check_collision(self, character):
        posible_moves = {
            'right': self.not_colliding('right', character),
            'left': self.not_colliding('left', character),
            'down': self.not_colliding('down', character),  
            'up': self.not_colliding('up', character)
        }
        return posible_moves

    def not_colliding(self, dir, character, in_battle=False):
        not_colliding = True
        speed = 32 if in_battle else character.speed
        r = character.rect.move(
            character.movement[dir][0] * speed,
            character.movement[dir][1] * speed
        )
        rect = character.get_hitbox(r)
        for col in self.colliders:
            if col.is_colliding(rect):
                not_colliding = False
        return not_colliding

    def blit_all_tiles(self, screen):
        for y in self.tiles:
            for x in y:
                for tile in x["layers"]:
                    if tile.exist:
                        self.blit_tile(tile, x["x"], x["y"], screen)
                        tile.update_frame_counter()
        for obj in self.objects:
            img = pygame.transform.scale(obj.image, (size, size))
            screen.blit(img, (obj.x, obj.y))
    
    def blit_overlay(self, player_rect, screen):
        x = int((player_rect.x + size / 2) // size)
        y = int((player_rect.y + size / 2) // size)
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
        transformed_image = pygame.transform.scale(img, (size, size))
        screen.blit(transformed_image, (x, y))

    def change_state(self, pos):
        x = int((pos[0] + size / 2) // size)
        y = int((pos[1] + size / 2) // size)
        dir = 'up'
        if dir == 'up':
            y -= 1
        for i, layer in enumerate(self.tiles[y - 1][x]["layers"]):
            if layer.type == "door":
                self.tiles[y][x]["layers"][i].change_state()

    def get_tile_grid(self):
        tiles = self.get_sceleton_grid()
        objects = []
        colliders = []
        for layer_index, layer in enumerate(self.tmxdata.layers):
            self.layers_amount = layer_index + 1
            if isinstance(layer, pytmx.TiledTileLayer):
                for tile in layer.tiles():
                    properties = self.tmxdata.get_tile_properties(tile[0], tile[1], layer_index)
                    properties["frame_images"] = [self.tmxdata.get_tile_image_by_gid(frame.gid) for frame in properties["frames"]]
                    tile_obj = Tile(tile, properties)
                    tiles[tile[1]][tile[0]]["layers"].append(tile_obj)
            elif isinstance(layer, pytmx.TiledObjectGroup):
                if layer.name == 'collision':
                    for col in layer:
                        colliders.append(Collider(col))
                else:
                    for obj in layer:
                        img = self.tmxdata.get_tile_image_by_gid(obj.gid)
                        map_object = MapObject(img, obj)
                        objects.append(map_object)
            else:
                print("Unrecognized layer type in get_tile_grid()")
        return tiles, objects, colliders
    
    def get_sceleton_grid(self):
        tiles = []
        for y in range(0, self.tmxdata.height):
            tiles.append([])
            for x in range(0, self.tmxdata.width):
                tiles[y].append({"x": x * size, "y": y * size, "layers": []})
        return tiles

class Collider:
    def __init__(self, obj, id=-1):
        self.id = id
        self.obj = obj
        self.rect = pygame.Rect(
            (obj.x * 2, obj.y * 2),
            (obj.width * 2, obj.height * 2)
        )
        self.is_polygon = hasattr(obj, "points")
        if self.is_polygon:
            self.x = min([p[0] for p in obj.points]) * 2
            self.y = min([p[1] for p in obj.points]) * 2
            self.dots = []
            self.get_dots(obj.points)
            self.rect = pygame.Rect((self.x, self.y), (size, size))

    def move(self, x, y, id):
        if self.id == id:
            self.rect = self.rect.move(x, y)

    def is_colliding(self, rect):
        if self.rect.colliderect(rect):
            if self.is_polygon:
                for point in self.dots:
                    if rect.colliderect(point):
                        return True
            else:
                return True
        return False

    def get_dots(self, points):
        points = [(p[0] * 2, p[1] * 2) for p in points]
        vartical_down = (self.x, self.y) in points and (self.x + size, self.y + size) in points
        for val in range(0, size):
            mod = val if vartical_down else size - val
            self.dots.append(pygame.Rect((self.x + mod, self.y + val), (1, 1)))

class MapObject(pygame.sprite.Sprite):
    def __init__(self, img, obj):
        super().__init__()
        self.x = obj.x * 2
        self.y = obj.y * 2
        self.rect = pygame.Rect((obj.x * 2, obj.y * 2), (size, size))
        self.image = pygame.transform.scale(img, (size, size))
        self.props = obj.properties
        if hasattr(obj.properties, "id"):
            self.id = obj.properties["id"]
        else:
            self.id = -1

class Tile(pygame.sprite.Sprite):
    def __init__(self, tmx_tile, properties):
        super().__init__()
        self.tmx_tile = tmx_tile
        self.x = tmx_tile[0]
        self.y = tmx_tile[1]
        self.image = pygame.transform.scale(tmx_tile[2], (size, size))
        properties = properties
        self.id = properties["id"]
        self.collision = properties["collision"]
        self.is_overlay = properties["is_overlay"]
        # Types: 'chest', 'summon', 'wall', 'door', 'object', 'ground'
        self.type = properties["type"] 
        self.value = properties["value"] 
        self.width = str(size)
        self.height = str(size) 
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
