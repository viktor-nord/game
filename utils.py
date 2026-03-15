import pygame

def get_adjasent_cord(pos, dir=None):
    x, y = pos[0], pos[1]
    dic = {
        'right': [x + 1, y],
        'left': [x - 1, y],
        'down': [x, y + 1],
        'up': [x, y - 1]
    }
    if dir:
        return dic[dir]
    else:
        return dic

def get_key_text(key):
    text = ''
    if key == pygame.K_RIGHT:
        text = 'right'
    elif key == pygame.K_LEFT:
        text = 'left'
    elif key == pygame.K_DOWN:
        text = 'down'
    elif key == pygame.K_UP:
        text = 'up'
    else:
        print('key missing in utils/get_key_text')
    return text
