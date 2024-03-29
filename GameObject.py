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
        player1 = Player1()
        player2 = Player2()
        animation1 = animation()
        animation2 = animation()
        spriteSheetEnv = pygame.image.load("Ressources/map_normal.png").convert()
        spriteSheetPlayer1 = pygame.image.load("Ressources/Personnage1.png")
        spriteSheetPlayer2 = pygame.image.load("Ressources/Personnage2.png")
        listeBullet = []
        bulletMouvement1 = bulletMouvement()
        countPlayer1 = 0
        countPlayer2 = 0
        gravite = 1

        return screen1, Clock, collision1, player1, player2, spriteSheetEnv, spriteSheetPlayer1, spriteSheetPlayer2, animation1, animation2, listeBullet, bulletMouvement1, countPlayer1, countPlayer2, gravite

    def loop(self):
        screen1, Clock, collision1, player1, player2, spriteSheetEnv, spriteSheetPlayer1, spriteSheetPlayer2, animation1, animation2, listeBullet, bulletMouvement1, countPlayer1, countPlayer2, gravite = self.variableInit()
        winner = ''

        quitGame = True
        while quitGame:
            Clock.tick(65)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quitGame = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        player1.playerJump(countPlayer1)
                        countPlayer1 += 1
                    if event.key == pygame.K_KP8:
                        player2.playerJump(countPlayer2)
                        countPlayer2 += 1

            screen1 = player1.playerMovement(gravite, screen1, (len(map4[0])*32), listeBullet)
            screen1 = player2.playerMovement(gravite, screen1, (len(map4[0])*32), listeBullet)
            player1, screen1, countPlayer1 = collision1.isCollided(player1, map4, screen1, countPlayer1)
            player2, screen1, countPlayer2 = collision1.isCollided(player2, map4, screen1, countPlayer2)
            bulletMouvement1.bulletAction(listeBullet, screen1, map4, player1, player2)
            winner = screen1.draw(player1, player2, map4, Clock, spriteSheetEnv, spriteSheetPlayer1, spriteSheetPlayer2, animation1, animation2, listeBullet)

            if winner != '':
                quitGame = False

        screen1 = pygame.display.set_mode((800, 600))
        return winner



class bulletMouvement:

    def __init__(self):
        pass

    def bulletAction(self, listeBullet, screen, map, player1, player2):
        self.bulletMouvement(listeBullet)
        self.bulletSuppr(listeBullet, screen, map, player1, player2)

    def bulletMouvement(self, listeBullet):
        for i in range(0, len(listeBullet)):
            listeBullet[i].avance()

    def bulletSuppr(self, listeBullet, screen, map, player1, player2):
        tampon = []
        collision = False
        for i in range(0, len(listeBullet)):
            collision = self.collisionBullet(listeBullet[i], map, screen, player1, player2)
            if listeBullet[i].posX < 0 or listeBullet[i].posX > screen.screenWidth or collision:
                tampon.append(i)

        for i in range(0, len(tampon)):
            del listeBullet[tampon[0]]

    def collisionBullet(self, bullet, map, screen, player1, player2):
        i = max(0, int((bullet.posX + 16 - screen.cameraPosX) // 32))
        j = max(0, int((bullet.posY + 16) // 32))
        if i == len(map[0]):
            i = len(map[0]) - 1

        if map[j][i] != -1:  #and map[j][i] != 13 and map[j][i] != 14 and map[j][i] != 15:
            return True
        elif (bullet.posX + 16 > player1.posX and bullet.posX + 16 < player1.posX + 32) and ((bullet.posY + 16 > player1.posY and bullet.posY + 16 < player1.posY + 32) or bullet.posY == player1.posY):
            player1.isDead = True
            return True
        elif (bullet.posX + 16 > player2.posX and bullet.posX + 16 < player2.posX + 32) and ((bullet.posY + 16 > player2.posY and bullet.posY + 16 < player2.posY + 32) or bullet.posY == player2.posY):
            player2.isDead = True
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
            self.posX = player1_posX + 32
            self.posY = player1_posY
        else:
            self.posX = player1_posX - 32
            self.posY = player1_posY
        self.direction = player1_direction

    def avance(self):
        if self.direction == 0:
            self.posX -= self.speed
        else:
            self.posX += self.speed



class Player1:

    oldPosX = 32
    oldPosY = 0
    posX = 32
    posY = 640
    size = 32
    speedX = 5
    speedY = 0
    isJumping = False
    isDoubleJumping = False
    isMoving = False
    direction = 1
    shootCount = 0
    countFall = 0
    isDead = False

    def __init__(self):
        pass

    def playerShoot(self, keyPressed, listeBullet):
        self.shootCount += 1
        if keyPressed[pygame.K_SPACE] and self.shootCount >= 20 and self.isDead == False:
            self.shootCount = 0
            bullet1 = bullet(self.posX, self.posY, self.direction)
            listeBullet.append(bullet1)

    def playerJump(self, count):
        if count < 2 and self.isDead == False:
            self.isJumping = True
            self.speedY = 0
            self.speedY -= 10

    def playerFall(self, gravite):
        self.countFall += 1

        if (self.countFall == 2):
            self.speedY += gravite
            self.countFall = 0
        
        self.speedY = min(25, self.speedY)

        self.posY += self.speedY

    def playerDeplacementGauche(self, keyPressed, screen1, mapWidth):
        if keyPressed[pygame.K_a] and self.posX > 0 and self.isDead == False: #--Gauche
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
        if keyPressed[pygame.K_d] and self.posX < (screen1.screenWidth - self.size) and self.isDead == False: #--Droite
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

        if keyPressed[pygame.K_d] == 0 and keyPressed[pygame.K_a] == 0:
            self.isMoving = False

        return screen1


class Player2:

    oldPosX = 1216
    oldPosY = 0
    posX = 1216
    posY = 640
    size = 32
    speedX = 5
    speedY = 0
    isJumping = False
    isDoubleJumping = False
    isMoving = False
    direction = 1
    shootCount = 0
    countFall = 0
    isDead = False

    def __init__(self):
        pass

    def playerShoot(self, keyPressed, listeBullet):
        self.shootCount += 1
        if keyPressed[pygame.K_KP0] and self.shootCount >= 20 and self.isDead == False:
            self.shootCount = 0
            bullet1 = bullet(self.posX, self.posY, self.direction)
            listeBullet.append(bullet1)

    def playerJump(self, count):
        if count < 2 and self.isDead == False:
            self.isJumping = True
            self.speedY = 0
            self.speedY -= 10

    def playerFall(self, gravite):
        self.countFall += 1

        if (self.countFall == 2):
            self.speedY += gravite
            self.countFall = 0
        
        self.speedY = min(25, self.speedY)

        self.posY += self.speedY

    def playerDeplacementGauche(self, keyPressed, screen1, mapWidth):
        if keyPressed[pygame.K_KP4] and self.posX > 0 and self.isDead == False: #--Gauche
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
        if keyPressed[pygame.K_KP6] and self.posX < (screen1.screenWidth - self.size) and self.isDead == False: #--Droite
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

        if keyPressed[pygame.K_KP4] == 0 and keyPressed[pygame.K_KP6] == 0:
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

    def drawPlayer(self, screen, player1, player2, spriteSheetPlayer1, spriteSheetPlayer2, animation1, animation2):
        animSprite1 = animation1.perso(player1)

        if(animSprite1 == -1):
            return 'ROUGE'

        animSprite2 = animation2.perso(player2)

        if(animSprite2 == -1):
            return 'BLEU'

        screen.blit(spriteSheetPlayer1, (player1.posX, player1.posY), (animSprite1 * 32, 0, 32, 32))
        screen.blit(spriteSheetPlayer2, (player2.posX, player2.posY), (animSprite2 * 32, 0, 32, 32))

        return ''

    def drawMap(self, screen, map, spriteSheetEnv):
        for i, ligne in enumerate(map):
            for j, case in enumerate(ligne):
                if (j*32 + self.cameraPosX) >= -32 and (j*32 + self.cameraPosX) < self.screenWidth:
                    screen.blit(spriteSheetEnv, (j*32 + self.cameraPosX, i*32), (case * 32, 0, 32, 32))

    def drawFont(self, screen, Clock):
        myfont = pygame.font.SysFont("monospace", 15)
        label = myfont.render("FPS : "+str(floor(Clock.get_fps())), 1, (255, 255, 255))
        screen.blit(label, (1200, 10))

    def drawBullet(self, screen, listeBullet, animation, spriteSheetPlayer1, spriteSheetPlayer2):
        for i in range(0, len(listeBullet)):
            animSprite = animation.bullet(listeBullet[i])
            screen.blit(spriteSheetPlayer1, (listeBullet[i].posX, listeBullet[i].posY), (animSprite * 32, 0, 32, 32))
            screen.blit(spriteSheetPlayer2, (listeBullet[i].posX, listeBullet[i].posY), (animSprite * 32, 0, 32, 32))

    def draw(self, player1, player2, map4, Clock, spriteSheetEnv, spriteSheetPlayer1, spriteSheetPlayer2, animation1, animation2, listeBullet):
        self.screen.fill((0,0,0))
        self.drawMap(self.screen, map4, spriteSheetEnv)
        self.drawFont(self.screen, Clock)
        winner = self.drawPlayer(self.screen, player1, player2, spriteSheetPlayer1, spriteSheetPlayer2, animation1, animation2)
        self.drawBullet(self.screen, listeBullet, animation1, spriteSheetPlayer1, spriteSheetPlayer2)
        pygame.display.flip()

        return winner



class animation:
    animSpritePerso = 0
    animSpriteBullet = 0
    compteurAnim = 0

    def __init__(self):
        pass

    def perso(self, player1):
        self.compteurAnim += 1
        if self.compteurAnim == 6:
            if player1.isDead == False:
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

            else:
                if self.animSpritePerso < 26:
                    self.animSpritePerso = 26
                elif self.animSpritePerso == 32:
                    return -1

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