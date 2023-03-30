import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join

import Player
import Block

pygame.init()

pygame.display.set_caption("Mario Platformer")

WIDTH, HEIGHT = 816, 600
FPS = 60
PLAYER_VELOCITY = 4.25

window = pygame.display.set_mode((WIDTH, HEIGHT))

def flipImage(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def loadSpriteSheets(dir1, dir2, w, h, direction = False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    allSprites = {}

    for image in images:
        spriteSheet = pygame.image.load(join(path, image)).convert_alpha()
        
        sprites = []
        for i in range(spriteSheet.get_width() // w):
            surface = pygame.Surface((w, h), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * w, 0, w, h)
            surface.blit(spriteSheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))
        
        if direction:
            allSprites[image.replace(".png", "") + "_right"] = sprites
            allSprites[image.replace(".png", "") + "_left"] = flipImage(sprites)
        else:
            allSprites[image.replace(".png", "")] = sprites
    
    return allSprites

def getBackground(name):
    image = pygame.image.load(join("assets", "backgrounds", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)
    
    return tiles, image

def draw(window, background, bgImage, player, blocks, offsetX):
    for tile in background:
        window.blit(bgImage, tile)

    for block in blocks:
        block.draw(window, offsetX)

    player.draw(window, offsetX)

    pygame.display.update()

def handleVerticalCollision(player, objects, dy):
    collidedObjects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hitHead()

        collidedObjects.append(obj)

    return collidedObjects

def handleHorizontalCollision(player, objects, dx):
    player.move(dx, 0)
    player.update()

    colidedObject = None

    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            colidedObject = obj
            break
    
    player.move(-dx, 0)
    player.update()

    return colidedObject

def handleMovement(player, objects):
    keys = pygame.key.get_pressed()
    
    player.x_vel = 0
    colideLeft = handleHorizontalCollision(player, objects, -PLAYER_VELOCITY)
    colideRight = handleHorizontalCollision(player, objects, PLAYER_VELOCITY)

    if (keys[pygame.K_a] and not colideLeft) or (keys[pygame.K_LEFT] and not colideLeft):
        player.moveLeft(PLAYER_VELOCITY)
    elif (keys[pygame.K_d] and not colideRight) or (keys[pygame.K_RIGHT] and not colideRight):
        player.moveRight(PLAYER_VELOCITY)
    
    handleVerticalCollision(player, objects, player.y_vel)

def main(window):
    clock = pygame.time.Clock()
    background, bgImage = getBackground("Brown.png")

    blockSize = 48

    player = Player.Player(500, 100, 32, 32)
    floor = [Block.Block(i * blockSize, HEIGHT - blockSize, blockSize) for i in range(-WIDTH // blockSize, (WIDTH*2) // blockSize)]
    objects = [*floor, Block.Block(0, HEIGHT - blockSize * 2, blockSize), Block.Block(blockSize * 3, HEIGHT - blockSize * 4, blockSize)]

    offsetX = 0
    scrollArea = 100

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
            if event.type == pygame.KEYDOWN:
                if event.key == (pygame.K_SPACE or pygame.K_UP or pygame.K_w):
                    player.jump()

        player.loop(FPS)
        handleMovement(player, objects)
        draw(window, background, bgImage, player, objects, offsetX)

        if ((player.rect.right - offsetX >= WIDTH - scrollArea) and player.x_vel > 0) or (
            (player.rect.left - offsetX <= scrollArea) and player.x_vel < 0):
            offsetX += player.x_vel
    
    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)