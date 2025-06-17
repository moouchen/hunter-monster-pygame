import pygame
pygame.init()

win = pygame.display.set_mode((500,480))

pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('images/R1.png'), pygame.image.load('images/R2.png'), pygame.image.load('images/R3.png'), pygame.image.load('images/R4.png'), pygame.image.load('images/R5.png'), pygame.image.load('images/R6.png'), pygame.image.load('images/R7.png'), pygame.image.load('images/R8.png'), pygame.image.load('images/R9.png')]
walkLeft = [pygame.image.load('images/L1.png'), pygame.image.load('images/L2.png'), pygame.image.load('images/L3.png'), pygame.image.load('images/L4.png'), pygame.image.load('images/L5.png'), pygame.image.load('images/L6.png'), pygame.image.load('images/L7.png'), pygame.image.load('images/L8.png'), pygame.image.load('images/L9.png')]
bg = pygame.image.load('images/bg.jpg')
char = pygame.image.load('images/standing.png')

clock = pygame.time.Clock()

score = 0
font = pygame.font.SysFont("comicsans", 30, True)

music = pygame.mixer.music.load('images/music.mp3')
pygame.mixer.music.play(-1)


class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x , self.y ,  40 , 40)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
        else:
            if self.right : 
                win.blit(walkRight[0], (self.x,self.y))
            else:
                win.blit(walkLeft[0], (self.x,self.y))
        self.hitbox = (self.x+18 , self.y+12 ,  28 , 52)

    def hit(self):
        global font,score
        if self.isJump :
            self.x = 60
            self.y = 360
        else :
            self.x = 60
            self.y =410 

        text = font.render("-5", True ,(255, 0, 0))
        win.blit(text,(255,230))
        pygame.display.update()
        i=0
        while i < 300:
            pygame.time.delay(1)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()
            

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 10 * facing

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

class enemy (object):
    def  __init__(self,x,y,width,height,end):
        self.walkRight = [pygame.image.load('images/R1E.png'), pygame.image.load('images/R2E.png'), pygame.image.load('images/R3E.png'), pygame.image.load('images/R4E.png'), pygame.image.load('images/R5E.png'), pygame.image.load('images/R6E.png'), pygame.image.load('images/R7E.png'), pygame.image.load('images/R8E.png'), pygame.image.load('images/R9E.png'), pygame.image.load('images/R10E.png'), pygame.image.load('images/R11E.png')]
        self.walkLeft = [pygame.image.load('images/L1E.png'), pygame.image.load('images/L2E.png'), pygame.image.load('images/L3E.png'), pygame.image.load('images/L4E.png'), pygame.image.load('images/L5E.png'), pygame.image.load('images/L6E.png'), pygame.image.load('images/L7E.png'), pygame.image.load('images/L8E.png'), pygame.image.load('images/L9E.png'), pygame.image.load('images/L10E.png'), pygame.image.load('images/L11E.png')]
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.damageCount = 0
        self.hitbox = (self.x+14 , self.y+7 ,  40 , 53)

    def draw(self):

        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        self.move()
        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1
        self.hitbox = (self.x+14 , self.y+7 ,  40 , 53)
        pygame.draw.rect(win, (0, 128 ,0), (self.x+15 , self.y-4 ,40, 5))
        pygame.draw.rect(win, (255, 0 ,0), (self.x+55-self.damageCount ,self.y-4 , self.damageCount , 5))



    def move(self):
        if self.vel > 0:
            if self.x  < self.path[1]:
                self.x += self.vel
            else :
                self.vel = self.vel * -1
                self.x +=self.vel
        elif self.vel < 0:
            if self.x  > self.path[0]:
                self.x += self.vel
            else :
                self.vel = self.vel * -1
                self.x+=self.vel

    def hit (self):
        global enemy1
        self.damageCount +=2
        if self.damageCount>= 40 :
            enemy1 = None


        

def redrawGameWindow():
    global score, font
    win.blit(bg, (0,0))
    man.draw(win)
    if enemy1 is not None :
        enemy1.draw()
    for bullet in bullets:
        bullet.draw(win)
    score_text = f"Score : {score}"
    text_surface = font.render(score_text, True, (0, 0, 0))
    win.blit(text_surface,(300  ,10))
    pygame.display.update()


#mainloop
enemy1 = enemy(0, 415, 64, 64, 450)
man = player(200, 410, 64,64)
run = True
bullets = []
shootingLoop = 0
while run:
    clock.tick(27)
    if enemy1 is not None:
        if man.y+man.height > enemy1.hitbox[1] and man.y + man.height< enemy1.hitbox[1]+enemy1.hitbox[3]:
            if man.x + man.width> enemy1.hitbox[0] and man.x+ man.width < enemy1.hitbox[0]+enemy1.hitbox[2]:
                man.hit()
                score-=5
    if shootingLoop > 0 : 
        shootingLoop+= 1
    if shootingLoop> 3 :
        shootingLoop =0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    for bullet in bullets:
        if enemy1 is not None :
            
            if bullet.x > enemy1.hitbox[0] and bullet.x < enemy1.hitbox[0]+enemy1.hitbox[2]:
                if bullet.y > enemy1.hitbox[1] and bullet.y< enemy1.hitbox[1]+enemy1.hitbox[3]:
                    enemy1.hit()
                    score += 1       

                    bullets.pop(bullets.index(bullet))

        if bullet.x < 500 and bullet.x > 0:
            bullet.x+= bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.walkCount = 0
        man.standing = True 
    
    if keys[pygame.K_SPACE] and shootingLoop == 0:
        if man.right :
            facing = 1
        else : facing = -1
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height//2), 6, (0,0,0), facing))
        shootingLoop = 1
    if not(man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
            
    redrawGameWindow()

pygame.quit()

#code by MOHAMED AMINE OUCHEN