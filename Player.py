import pygame
from main import loadSpriteSheets

class Player(pygame.sprite.Sprite):
    GRAVITY = 1
    SPRITES = loadSpriteSheets("MainCharacters", "NinjaFrog", 32, 32, True)
    ANIMATION_DELAY = 2
    
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animationCount = 0
        self.fallCount = 0
        self.count = 0
        self.isTouchingGround = False

    def jump(self):
        if self.isTouchingGround:
            self.y_vel = -self.GRAVITY * 8
            self.animationCount = 0
            self.isTouchingGround = False
        
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    
    def moveLeft(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animationCount = 0

    def moveRight(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animationCount = 0
    
    def landed(self):
        self.fallCount = 0
        self.y_vel = 0
        self.isTouchingGround = True


    def hitHead(self):
        self.y_vel *= -1
    
    def loop(self, fps):
        self.y_vel += min(1, (self.fallCount / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        self.fallCount += 1
        self.updateSprite()

    def updateSprite(self):
        spriteSheet = "idle"
        if self.y_vel < 0:
            spriteSheet = "jump"
        elif self.y_vel > 0 and not self.isTouchingGround:
            spriteSheet = "fall"
        elif self.x_vel != 0:
            spriteSheet = "run"
        
        spriteSheetName = spriteSheet + "_" + self.direction
        sprites = self.SPRITES[spriteSheetName]
        spriteIndex = (self.animationCount // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[spriteIndex]
        self.animationCount += 1
        self.update()
    
    def update(self):
        self.rect = self.sprite.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, window, offsetX):
        window.blit(self.sprite, (self.rect.x - offsetX, self.rect.y))