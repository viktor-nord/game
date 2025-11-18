class Funk():
    def __init__(self, game):
        self.game = game
        self.base_tile_prop = {
            'id': -1, 
            'collision': 0, 
            'type': 'fake', 
            'source': '', 
            'trans': None, 
            'width': '32', 
            'height': '32', 
            'frames': []
        }

    def try_get_prop(self, x, y, layer=0):
        try:
            properties = self.game.tmxdata.get_tile_properties(x, y, layer)
        except ValueError:
            properties = self.base_tile_prop
        if properties is None:
            properties = self.base_tile_prop
        return properties
