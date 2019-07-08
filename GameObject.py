#coding:utf-8

import pygame
from os import environ
from math import floor
from Map import *

class gameLoop:

    def __init__(self):
        pygame.init()
        pygame.font.init()

    def variableInit(self):
        screen1 = screen()
        Clock = pygame.time.Clock()
        collision1 = collision()
        player1 = player()
        animation1 = animation()
        spriteSheetEnv = pygame.image.load("Ressources/Environnement3.png").convert()
        spriteSheetPlayer = pygame.image.load("Ressources/Personnage.png")
        listeBullet = []
        bulletMouvement1 = bulletMouvement()
        count = 0
        gravite = 2

        return screen1, Clock, collision1, player1, spriteSheetEnv, spriteSheetPlayer, animation1, listeBullet, bulletMouvement1, count, gravite

    def loop(self):
        screen1, Clock, collision1, player1, spriteSheetEnv, spriteSheetPlayer, animation1, listeBullet, bulletMouvement1, count, gravite = self.variableInit()

        quitGame = True
        while quitGame:
            Clock.tick(65)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quitGame = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        player1.playerJump(count)
                        count += 1

            screen1 = player1.playerMovement(gravite, screen1, (len(map3[0])*32), listeBullet)
            player1, screen1, count = collision1.isCollided(player1, map3, screen1, count)
            bulletMouvement1.bulletAction(listeBullet, screen1, map3)
            screen1.draw(player1, map3, Clock, spriteSheetEnv, spriteSheetPlayer, animation1, listeBullet)

        pygame.quit()



class bulletMouvement:

    def __init__(self):
        pass

    def bulletAction(self, listeBullet, screen, map):
        self.bulletMouvement(listeBullet)
        self.bulletSuppr(listeBullet, screen, map)

    def bulletMouvement(self, listeBullet):
        for i in range(0, len(listeBullet)):
            listeBullet[i].avance()

    def bulletSuppr(self, listeBullet, screen, map):
        tampon = []
        collision = False
        for i in range(0, len(listeBullet)):
            collision = self.collisionBullet(listeBullet[i], map, screen)
            if listeBullet[i].posX < 0 or listeBullet[i].posX > screen.screenWidth or collision:
                tampon.append(i)

        for i in range(0, len(tampon)):
            del listeBullet[tampon[i]]

    def collisionBullet(self, bullet, map, screen):
        i = max(0, int((bullet.posX - screen.cameraPosX) // 32))
        j = max(0, int((bullet.posY) // 32))
        if i == len(map[0]):
            i = len(map[0]) - 1

        if map[j][i] != -1 and map[j][i] != 13 and map[j][i] != 14 and map[j][i] != 15:
            return True
        else:
            return False


class bullet:
    posX = 0
    posY = 0
    direction = 0
    speed = 12

    def __init__(self, player1_posX, player1_posY, player1_direction):
        if player1_direction == 1:
            self.posX = player1_posX + 16
            self.posY = player1_posY
        else:
            self.posX = player1_posX - 16
            self.posY = player1_posY
        self.direction = player1_direction

    def avance(self):
        if self.direction == 0:
            self.posX -= self.speed
        else:
            self.posX += self.speed



class player:

    oldPosX = 32
    oldPosY = 0
    posX = 32
    posY = 640
    size = 32
    speedX = 3
    speedY = 0
    isJumping = False
    isDoubleJumping = False
    isMoving = False
    direction = 1
    shootCount = 0

    def __init__(self):
        pass

    def playerShoot(self, keyPressed, listeBullet):
        self.shootCount += 1
        if keyPressed[pygame.K_SPACE] and self.shootCount >= 20:
            self.shootCount = 0
            bullet1 = bullet(self.posX, self.posY, self.direction)
            listeBullet.append(bullet1)

    def playerJump(self, count):
        if count < 2:
            self.isJumping = True
            self.speedY = 0
            self.speedY -= 25

    def playerFall(self, gravite):
        self.speedY += gravite
        self.speedY = min(20, self.speedY)
        self.posY += self.speedY

    def playerDeplacementGauche(self, keyPressed, screen1, mapWidth):
        if keyPressed[pygame.K_a] and self.posX > 0: #--Gauche
            self.direction = 0
            self.isMoving = True
            if screen1.cameraPosX == 0 or self.posX - screen1.cameraPosX > mapWidth - (screen1.screenWidth / 2):
                self.posX -= self.speedX
            else:
                screen1.cameraPosX += self.speedX
        elif self.posX < 0:
            self.posX = 0

        return screen1

    def playerDeplacementDroite(self, keyPressed, screen1, mapWidth):
        if keyPressed[pygame.K_d] and self.posX < (screen1.screenWidth - self.size): #--Droite
            self.direction = 1
            self.isMoving = True
            if self.posX < (screen1.screenWidth / 2) or self.posX - screen1.cameraPosX >= mapWidth - (screen1.screenWidth / 2):
                self.posX += self.speedX
            else:
                screen1.cameraPosX -= self.speedX
        elif self.posX > (screen1.screenWidth - self.size):
            self.posX = screen1.screenWidth - self.size

        return screen1

    def playerMovement(self, gravite, screen1, mapWidth, listeBullet):
        keyPressed = pygame.key.get_pressed()
        self.oldPosX = self.posX
        self.oldPosY = self.posY
        screen1.oldCameraPosX = screen1.cameraPosX

        self.playerShoot(keyPressed, listeBullet)
        self.playerFall(gravite)
        screen1 = self.playerDeplacementGauche(keyPressed, screen1, mapWidth)
        screen1 = self.playerDeplacementDroite(keyPressed, screen1, mapWidth)

        if keyPressed[pygame.K_d] == 0 and keyPressed[pygame.K_a ] == 0:
            self.isMoving = False

        return screen1



class screen:
    screen = 0
    cameraPosX = 0
    oldCameraPosX = 0
    screenWidth = 1280
    screenHeight = 768
    black = (0, 0, 0)
    white = (255, 255, 255)
    oldMap = list()
    init = 0

    def __init__(self):
        environ['SDL_VIDEO_WINDOW_POS'] = "125, 40"
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption("Test jeux 1 Python")

    def drawPlayer(self, screen, player1, spriteSheetPlayer, animation):
        animSprite = animation.perso(player1)
        screen.blit(spriteSheetPlayer, (player1.posX, player1.posY), (animSprite * 32, 0, 32, 32))

    def drawMap(self, screen, map, spriteSheetEnv):
        for i, ligne in enumerate(map):
            for j, case in enumerate(ligne):
                if (j*32 + self.cameraPosX) >= -32 and (j*32 + self.cameraPosX) < self.screenWidth:
                    screen.blit(spriteSheetEnv, (j*32 + self.cameraPosX, i*32), (case * 32, 0, 32, 32))

    def drawFont(self, screen, Clock):
        myfont = pygame.font.SysFont("monospace", 15)
        label = myfont.render("FPS : "+str(floor(Clock.get_fps())), 1, (255, 255, 255))
        screen.blit(label, (1200, 10))

    def drawBullet(self, screen, listeBullet, animation, spriteSheetPlayer):
        for i in range(0, len(listeBullet)):
            animSprite = animation.bullet(listeBullet[i])
            screen.blit(spriteSheetPlayer, (listeBullet[i].posX, listeBullet[i].posY), (animSprite * 32, 0, 32, 32))

    def draw(self, player1, map, Clock, spriteSheetEnv, spriteSheetPlayer, animation, listeBullet):
        self.screen.fill((0,0,0))
        self.drawMap(self.screen, map, spriteSheetEnv)
        self.drawFont(self.screen, Clock)
        self.drawPlayer(self.screen, player1, spriteSheetPlayer, animation)
        self.drawBullet(self.screen, listeBullet, animation, spriteSheetPlayer)
        pygame.display.flip()



class animation:
    animSpritePerso = 0
    animSpriteBullet = 0
    compteurAnim = 0

    def __init__(self):
        pass

    def perso(self, player1):
        self.compteurAnim += 1
        if self.compteurAnim == 6:

            if player1.isJumping:
                if player1.direction == 0:
                    if self.animSpritePerso < 13 or self.animSpritePerso >= 17:
                        self.animSpritePerso = 13
                else:
                    if self.animSpritePerso < 1 or self.animSpritePerso >= 5:
                        self.animSpritePerso = 1
            elif player1.isMoving:
                if player1.direction == 0:
                    if self.animSpritePerso < 17 or self.animSpritePerso >= 23:
                        self.animSpritePerso = 17
                else:
                    if self.animSpritePerso < 5 or self.animSpritePerso >= 11:
                        self.animSpritePerso = 5
            else:
                if player1.direction == 0:
                    self.animSpritePerso = 11
                else:
                    self.animSpritePerso = -1

            self.animSpritePerso += 1
            self.compteurAnim = 0

        return self.animSpritePerso

    def bullet(self, bullet):
        if bullet.direction == 0:
            self.animSpriteBullet = 25
        else:
            self.animSpriteBullet = 24

        return self.animSpriteBullet



class collision:

    def __init__(self):
        pass

    def isCollided(self, player1, map, screen1, count):
        old_rect = pygame.Rect((player1.oldPosX - screen1.oldCameraPosX, player1.oldPosY), (32, 32))
        new_rect = pygame.Rect((player1.posX - screen1.cameraPosX, player1.posY), (32, 32))
        collide_later = list()

        i, j = self.coordToGrid(player1, screen1)
        blocks = self.neighbourBlock(i, j, map, player1, screen1)
        collide_later, player1, screen1, new_rect, count = self.collideOneAxe(collide_later, blocks, new_rect, old_rect, player1, screen1, map, count)
        player1, screen1, count = self.collideSecondAxe(collide_later, blocks, new_rect, old_rect, player1, screen1, map, count)

        if player1.speedY > 0:
            player1.isJumping = True

        return player1, screen1, count

    def collideOneAxe(self, collide_later, blocks, new_rect, old_rect, player1, screen1, map, count):
        dy_correction = 0
        for block in blocks:
            if not new_rect.colliderect(block):
                continue

            dx_correction, dy_correction = self.compute_penetration(block, old_rect, new_rect)
            if dx_correction == 0.0:
                new_rect.top += dy_correction
                player1.posY += dy_correction
                player1.speedY = 0.0
            elif dy_correction == 0.0:
                if player1.direction == 0:
                    if screen1.cameraPosX == 0 or player1.posX - screen1.cameraPosX > (len(map[0])*32) - (screen1.screenWidth / 2):
                        player1.posX += dx_correction
                    else:
                        screen1.cameraPosX -= dx_correction
                else:
                    if player1.posX < (screen1.screenWidth / 2) or player1.posX - screen1.cameraPosX >= (len(map[0])*32) - (screen1.screenWidth / 2):
                        player1.posX += dx_correction
                    else:
                        screen1.cameraPosX -= dx_correction
                new_rect.left += dx_correction
            else:
                collide_later.append(block)

        if(dy_correction < 0):
            player1.isJumping = False
            count = 0

        return collide_later, player1, screen1, new_rect, count

    def collideSecondAxe(self, collide_later, blocks, new_rect, old_rect, player1, screen1, map, count):
        dy_correction = 0
        for block in collide_later:
            dx_correction, dy_correction = self.compute_penetration(block, old_rect, new_rect)
            if dx_correction == dy_correction == 0.0:
                continue
            if abs(dx_correction) < abs(dy_correction):
                dy_correction = 0.0
            elif abs(dy_correction) < abs(dx_correction):
                dx_correction = 0.0
            if dy_correction != 0.0:
                player1.posY += dy_correction
                player1.speedY = 0.0
            elif dx_correction != 0.0:
                if player1.direction == 0:
                    if screen1.cameraPosX == 0 or player1.posX - screen1.cameraPosX > (len(map[0])*32) - (screen1.screenWidth / 2):
                        player1.posX += dx_correction
                    else:
                        screen1.cameraPosX -= dx_correction
                else:
                    if player1.posX < (screen1.screenWidth / 2) or player1.posX - screen1.cameraPosX >= (len(map[0])*32) - (screen1.screenWidth / 2):
                        player1.posX += dx_correction
                    else:
                        screen1.cameraPosX -= dx_correction
                new_rect.left += dx_correction

        if dy_correction < 0:
            player1.isJumping = False
            count = 0

        return player1, screen1, count

    def coordToGrid(self, player1, screen1):
        i = max(0, int((player1.posX - screen1.cameraPosX) // 32))
        j = max(0, int(player1.posY // 32))
        return i, j

    def neighbourBlock(self, i_start, j_start, map, player1, screen1):
        blocks = list()
        for j in range(j_start, j_start+2):
            if (player1.posX >= screen1.screenWidth - 32):
                if map[j][i_start] != -1:#and map[j][i_start] != 13 and  map[j][i_start] != 14 and  map[j][i_start] != 15
                    topleft = i_start*32, j*32
                    blocks.append(pygame.Rect((topleft), (32, 32)))
            else:
                for i in range(i_start, i_start+2):
                    if map[j][i] != -1:#and map[j][i] != 13 and map[j][i] != 14 and map[j][i] != 15
                        topleft = i*32, j*32
                        blocks.append(pygame.Rect((topleft), (32, 32)))
        return blocks

    def compute_penetration(self, block, old_rect, new_rect):
        dx_correction = dy_correction = 0.0
        if old_rect.bottom <= block.top < new_rect.bottom: #collision en bas
            dy_correction = block.top - new_rect.bottom
        elif old_rect.top >= block.bottom > new_rect.top: #collison en haut
            dy_correction = block.bottom - new_rect.top
        if old_rect.right <= block.left < new_rect.right: #collison à droite
            dx_correction = block.left - new_rect.right
        elif old_rect.left >= block.right > new_rect.left: #collision à gauche
            dx_correction = block.right - new_rect.left
        return dx_correction, dy_correction
