import pygame, math, random

# initialize the pygame
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
frameRate = 60
# create the screen
X = 800
Y = 600
screen = pygame.display.set_mode((X, Y))
white = (255, 255, 255)
lightGrey = (211, 211, 211)
silver = (192, 192, 192)
darkGrey = (169, 169, 169)
gray = (150, 150, 150)
green = (0, 192, 0)
darkGreen = (0, 150, 0)

#music
#music = pygame.mixer.music.load('music.mp3')                        #music by the Deli - 5:32PM
#pygame.mixer.music.play(-1)

#sound effects
boomSound = pygame.mixer.Sound('boomSound.wav')
boomSound.set_volume(20)
launchSound = pygame.mixer.Sound('launchSound.wav')
launchSound.set_volume(.1)

# title and icon
pygame.display.set_caption("Moon Shot")
icon = pygame.image.load('icon.png').convert_alpha()
pygame.display.set_icon(icon)

###########################################################################################################
# class system for objects: rocket, moon, earth
class object:
    def __init__(self, name):
        self.name = name
        self.pos = []
        self.vel = []
        self.acc = []
        self.angle = 0
        self.rot = 0
        self.hitbox = []

# planet creation
earth = object('earth')
earth.pos = [345, 320]
earthImg = pygame.image.load('earth100.png').convert()

# rocket creation
rocket = object('rocket')
rocket.angle = 0
rocket.pos = [395, 320]
rocket.vel = [0, 0]
rocket.launchVel = 3
rocket.acc = [0, 0]
rocketImg = pygame.image.load('rocket32.png').convert_alpha()
rocketExist = True
rocketMotion = False

# rocket explosion animation
explosion_anim = []
expl = ""
for i in range(6):
    filename = 'explosion{}.png'.format(i)
    fileupload = pygame.image.load(filename).convert_alpha()
    explosion_anim.append(fileupload)

class boom(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 5
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame < len(explosion_anim):
                pos = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = pos 

# moon creation
moon = object('moon')
moon.pos = [400, 100]
moon.rot = 1
moon.angle = 0
moonImg = pygame.image.load('moon70.png').convert_alpha()
moonImgCopy = moonImg.copy()
moon_rect = moonImg.get_rect(center = moon.pos)

# orbit creation
moon.orbitRadius = 200
moon.orbitAngle = 0
moon.orbitCenter = [400, 340]

# star creation
class shine():                                                             # basically, this is the same animation code
    def __init__(self, pos):                                               # as the start up message, but I added the animList
        pygame.sprite.Sprite.__init__(self)                                # as part of the object initialization
                                                                           # this is so that each object in the starObjectList has
        self.anim = []                                                     # its own animation list to iterate through
        for i in range(3):
            filename = 'star{}.png'.format(i)
            fileupload = pygame.image.load(filename).convert_alpha()
            self.anim.append(fileupload)

        self.image = self.anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 300

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
def starLoc():                                                          # this function just gives a list of 10(starCount)
    xScreen = list(range(100, 700))                                     # random locations using the random module
    yScreen = list(range(100, 500))
    starPosList = []
    starCount = 10
    counter = 0
    while counter <= starCount:
        counter += 1
        starPos = (random.choice(xScreen), random.choice(yScreen))
        xScreen.remove(starPos[0])                                      #this makes sure no two stars are in the same pos
        yScreen.remove(starPos[1])
        starPosList.append(starPos)
    return starPosList   
starPosList = starLoc()

starObjectList = []
for starPos in starPosList:
    starObjectList.append(shine(starPos))  

# distance function to be used to detect for collision
def distance(x1, y1, x2, y2):
    D = math.hypot(abs(x2-x1), abs(y2-y1))
    return D

def rocketReset():
    rocket.pos = [395, 320]
    rocket.vel = [0, 0]
    rocket.acc = [0, 0]
    rocket.angle = 0
    screen.blit(rocketImgCopy, rocket_rect)

###########################################################################################################
 
# start message
def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface

class animMessage(pygame.sprite.Sprite):
    def __init__(self, text, file, size, pos):  #ex: ("moonshot", "ARCADECLASSIC.ttf", 75, (x, y))
        pygame.sprite.Sprite.__init__(self)

        self.anim = []
        colorList = [white, lightGrey, silver, darkGrey, gray, darkGrey, silver, lightGrey]
        for i in colorList:
            x = pygame.font.Font(file, size)
            self.anim.append(text_objects(text, x, i))

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
startMessage = animMessage("Moon Shot", "ARCADECLASSIC.ttf", 75, (X/2, Y/2))
started = False

# stat messages
class statMessage(pygame.sprite.Sprite):
    def __init__(self, text, file, size, pos):  #ex: ("moonshot", "ARCADECLASSIC.ttf", 75, (x, y))
        pygame.sprite.Sprite.__init__(self)

        self.image = text_objects(text, pygame.font.Font(file, size), white)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100

    def update(self, text, file, size):
        self.image = text_objects(text, pygame.font.Font(file, size), white)


# data message
rocketLvMessage = statMessage("launch velocity = " + str(rocket.launchVel), "type_writer.ttf", 10, (70, 15))        #"message + stat", font, size, position
rocketVelMessage = statMessage("rocket velocity = " + str(rocket.vel), "type_writer.ttf", 10, (80, 45))
moonPosMessage = statMessage("moon orbit angle to earth in deg. = " + str(moon.orbitAngle), "type_writer.ttf", 10, (122, 60))
frameRateMessage = statMessage("FPS: " + str(frameRate), "type_writer.ttf", 10, (760, 15))

# button class
class button():
    def __init__(self, color, file, text, size = 10, width = 0, height = 0, pos = (0, 0)):
        self.color = color
        self.pos = pos
        self.size = size
        self.width = width
        self.height = height
        self.text = text
        self.file = file
        self.rect = (self.pos[0], self.pos[1], self.width, self.height)
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        
        if self.text != '':
            message = text_objects(self.text, pygame.font.Font(self.file, self.size), white)
            screen.blit(message, (self.pos[0] + (self.width/2 - message.get_width()/2), self.pos[1] + (self.height/2 - message.get_height()/2)))

# initializing buttons launch increase, launch decrease, fps change
LvUp = button(green, "type_writer.ttf", "+", 10, 10, 10, (30, 25))
LvDown = button(green, "type_writer.ttf", "-", 10, 10, 10, (10, 25))
fpsUp = button(green, "type_writer.ttf", "+", 10, 10, 10, (770, 25))
fpsDown =  button(green, "type_writer.ttf", "-", 10, 10, 10, (750, 25))
fpsReset = button(green, "type_writer.ttf", "R", 10, 10, 10, (770, 40))
launch = button(green, "type_writer.ttf", "LAUNCH", 20, 100, 25, (345, 450))

# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # setting background of screen to black.
    screen.fill((0, 0, 0))
    
    # creating stars
    if starObjectList[0].frame < len(starObjectList[0].anim):                     # checks if the first star has iterated through list
        for i in range(len(starObjectList) - 1):                                  # blits and then updates all stars if true^
            screen.blit(starObjectList[i].image, starObjectList[i].rect)
            starObjectList[i].update()

    # Start Message Loop
    if started == False:
        if startMessage.frame <= len(startMessage.anim):
            startMessage.update()
        elif startMessage.frame > len(startMessage.anim):
            startMessage.frame = 0
        screen.blit(startMessage.image, startMessage.rect)
    
    # stat messages in top left
    rocketLvMessage.update("launch velocity = ({0:.3f})".format(rocket.launchVel), "type_writer.ttf", 10)
    screen.blit(rocketLvMessage.image, rocketLvMessage.rect)
    rocketVelMessage.update("rocket velocity = ({0:.3f}, {1:.3f})".format(rocket.vel[0], rocket.vel[1]), "type_writer.ttf", 10)
    screen.blit(rocketVelMessage.image, rocketVelMessage.rect)
    moonPosMessage.update("moon orbit angle to earth in deg. = {0:.0f}".format(-((moon.orbitAngle*180/math.pi) % 360)), "type_writer.ttf", 10)
    screen.blit(moonPosMessage.image, moonPosMessage.rect)
    frameRateMessage.update("FPS: {0:.1f}".format(frameRate), "type_writer.ttf", 10)
    screen.blit(frameRateMessage.image, frameRateMessage.rect)

    # interactive element; hoping to create touch screen interaction with rasberry pi interaction
    mousePos = pygame.mouse.get_pos()

    # button interaction for launch velocity of rocket
    LvUp.draw(screen)
    LvDown.draw(screen)

    if pygame.Rect(LvUp.rect).collidepoint(mousePos):
        LvUp.color = darkGreen
        if pygame.mouse.get_pressed()[0]:
            rocket.launchVel += .01
    else:
        LvUp.color = green
    if pygame.Rect(LvDown.rect).collidepoint(mousePos):
        LvDown.color = darkGreen
        if pygame.mouse.get_pressed()[0]:
            if rocket.launchVel > .01:
                rocket.launchVel -= .01
    else:
        LvDown.color = green

    # button interaction for fps
    fpsUp.draw(screen)
    fpsDown.draw(screen)
    fpsReset.draw(screen)

    if pygame.Rect(fpsUp.rect).collidepoint(mousePos):              #checks if mouse is on top of button
        fpsUp.color = darkGreen                                     #changes button color
        if pygame.mouse.get_pressed()[0]:                           #performs action if L-Click
            frameRate += .1
    if pygame.Rect(fpsDown.rect).collidepoint(mousePos):
        fpsDown.color = darkGreen
        if pygame.mouse.get_pressed()[0]:
            if frameRate > 20:
                frameRate -= .1
    if pygame.Rect(fpsReset.rect).collidepoint(mousePos):
        fpsReset.color = darkGreen
        if pygame.mouse.get_pressed()[0]:
            frameRate = 60

    else:
        fpsUp.color = green
        fpsDown.color = green
        fpsReset.color = green

    # rocket motion

    launch.draw(screen)
    if pygame.Rect(launch.rect).collidepoint(mousePos):
        launch.color = darkGreen
        if pygame.mouse.get_pressed()[0]:
            started = True
            if rocketMotion == False:
                rocket.vel[1] = rocket.launchVel
                pygame.mixer.Sound.play(launchSound)
                rocketMotion = True
    else:
        launch.color = green

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            started = True
            if rocketMotion == False:
                rocket.vel[1] = rocket.launchVel
                pygame.mixer.Sound.play(launchSound)
                rocketMotion = True



    #rotating moon
    moonImgCopy = pygame.transform.rotate(moonImg, moon.angle)      #rotates the moonImgCopy
    moon_rect = moonImgCopy.get_rect(center = moon.pos)             #creates a rectangle centered on the position of the moon
    moon.angle -= (1 % 360)*(.56779)                                #this is an arbitrary value founded empirically
    
    # orbitting moon and event triggers
    moon.pos = [(moon.orbitRadius*math.cos(moon.orbitAngle) + moon.orbitCenter[0]), (moon.orbitRadius*math.sin(moon.orbitAngle) + moon.orbitCenter[1])]
    moon.orbitAngle += (1 % 360)*.01

    # hit boxes for: rocket, moon, and event triggers
    rocket.hitbox = (rocket.pos[0] - 5, rocket.pos[1], 10, 10)  # - 5 for adjustment

    "pygame.draw.rect(screen, (255, 0, 0), rocket.hitbox, 2)"
    "pygame.draw.circle(screen, (0, 0, 255), [int(moon.pos[0] - 1), int(moon.pos[1])] , 38, 2)"   

    #this gives a distance between the rocket hitbox and the moonhitbox at all times
    rHitCenter = [rocket.hitbox[0] + 3, rocket.hitbox[1] + 3]
    rMdist = distance(rHitCenter[0], rHitCenter[1], moon.pos[0], moon.pos[1])
    dirRocketMoon = [(moon.pos[0] - rHitCenter[0]), (moon.pos[1] - rHitCenter[1])]
    if rocketMotion == True:
        rocket.acc[0] = 1400 * dirRocketMoon[0]/(pow(rMdist, 3))
        rocket.acc[1] = 1400 * dirRocketMoon[1]/(pow(rMdist, 3))
        rocket.vel[0] += rocket.acc[0]
        rocket.vel[1] -= rocket.acc[1]
        rocket.pos[0] += rocket.vel[0]
        rocket.pos[1] -= rocket.vel[1]
        rocket.angle = math.degrees(math.atan2(rocket.vel[1], rocket.vel[0]) - (math.pi / 2))
    if rocket.pos[1] <= 0 or rocket.pos[1] >= 600 or rocket.pos[0] <= 0 or rocket.pos[0] >= 800:
        rocketMotion = False
        rocketReset()
    if rMdist < 38:                   # the radius of the moon is 38 pixels
        rocket.vel = [0, 0]           # if a collision is detected, stop motion and blit of rocket
        if expl == "":
            expl = boom(rHitCenter)
            pygame.mixer.Sound.play(boomSound)
        rocketExist = False
        rocketMotion = False

    # putting objects on the screen
    screen.blit(earthImg, earth.pos)
    screen.blit(moonImgCopy, moon_rect)   # blits the rotating moon on the orbitting rectangle

    #blits rocket
    if rocketExist == True:
        rocketImgCopy = pygame.transform.rotate(rocketImg, rocket.angle)
        rocket_rect = rocketImgCopy.get_rect(center = rocket.pos)
        screen.blit(rocketImgCopy, rocket_rect)
    else:
        if expl.frame < len(explosion_anim):
            expl.update()
            screen.blit(expl.image, expl.rect)
            if expl.frame == (len(explosion_anim) - 1):
                rocketExist = True
                rocketMotion = False
                rocketReset()
                expl = ""
    # set fps
    clock.tick(frameRate)

    pygame.display.update()



