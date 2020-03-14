import pygame, math, random
# initialize
pygame.init()

bg = (0, 0, 0)
white = (255, 255, 255)
lightGrey = (211, 211, 211)
silver = (192, 192, 192)
darkGrey = (169, 169, 169)
gray = (128, 128, 128)

size = [800, 600]
screen = pygame.display.set_mode(size)
screen.fill(bg)
pygame.display.set_caption("jedi tests gravity")
clock = pygame.time.Clock()

class shine():
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)

        self.anim = []
        for i in range(3):
            filename = 'star{}.png'.format(i)
            fileupload = pygame.image.load(filename).convert_alpha()
            self.anim.append(fileupload)

        self.image = self.anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame < len(self.anim):
                pos = self.rect.center
                self.image = self.anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = pos
            elif self.frame > len(self.anim) - 1:
                self.frame = 0
def starLoc():
    xScreen = list(range(10, 791))
    yScreen = list(range(10, 591))
    starPosList = []
    starCount = 10
    counter = 1
    while counter <= starCount:
        counter += 1
        starPos = (random.choice(xScreen), random.choice(yScreen))
        xScreen.remove(starPos[0])
        yScreen.remove(starPos[1])
        starPosList.append(starPos)
    return starPosList   
starPosList = starLoc()

starObjectList = []
for starPos in starPosList:
    starObjectList.append(shine(starPos))  

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface

class Message(pygame.sprite.Sprite):
    def __init__(self, text, pos):
        pygame.sprite.Sprite.__init__(self)

        self.anim = []
        colorList = [white, lightGrey, silver, darkGrey, gray, darkGrey, silver, lightGrey]
        for i in colorList:
            largeText = pygame.font.Font('ARCADECLASSIC.ttf', 100)
            self.anim.append(text_objects(text, largeText, i))

        self.image = self.anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame < len(self.anim):
                pos = self.rect.center
                self.image = self.anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = pos
startMessage = Message("Moon Shot", (size[0]/2, size[1]/2))
started = False

done = False

#game loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                started = True

    screen.fill(bg)

    if starObjectList[0].frame < len(starObjectList[0].anim):
        for i in range(len(starObjectList) - 1):
            screen.blit(starObjectList[i].image, starObjectList[i].rect)
            starObjectList[i].update()




    if startMessage.frame <= len(startMessage.anim):
        startMessage.update()
        if started == False:
            screen.blit(startMessage.image, startMessage.rect)
    elif startMessage.frame > len(startMessage.anim):
        startMessage.frame = 0

    pygame.display.update()
pygame.quit()