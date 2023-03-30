from Object import *
from os.path import join

def loadBlock(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    # change coords to change image
    rect = pygame.Rect(96, 0, size, size)
    
    surface.blit(image, (0, 0), rect)
    return surface

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = loadBlock(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
