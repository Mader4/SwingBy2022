import time, random, math, os
import pygame

pygame.init()

class Game:
    def __init__(self, width, height, fps, tps):
        global game
        game = self

        #initializers
        self.setFrame(width, height)
        self.objects = []
        self.menuElements = []
        self.run = True
        #inputs
        self.keys = [False for i in range(7)]
        self.keyPresses = []
        self.mx, self.my = 0,0
        self.backGroundColor = (0,0,0)
        self.currentStage = -1
        #zoom
        self.zoom = 1
        self.move = True
        #username
        self.username = "Guest"
        self.textCaches = []
        #tickControl
        self.time, self.lastTime = 0,0
        self.tps, self.fps = tps, fps
        self.setFrameRate(fps, tps)
        self.showFPS = True
        #init
        self.setWindow()
    def setFrame(self, width, height):
        self.width, self.height = width, height
        self.xCenter, self.yCenter = width//2, height//2
    def map(self, x,y):
        return self.xCenter + x*self.zoom, self.yCenter*self.zoom
    def setFrameRate(self, fps, tps):
        self.tickTime = 1/tps
        self.frameTime = 1/fps
        self.FPS, self.TPS = 0,0
    def fpsUpdate(self):
        self.menuElements[0].text = "FPS: "+str(self.FPS)+", "+str(self.TPS) if self.showFPS else ""
        self.menuElements[0].paint()
    def setWindow(self):
        self.win = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.font = pygame.font.SysFont("Times New Roman",30)
        self.windowUpdate()
    def windowUpdate(self):
        pass
    def tick(self, events):
        self.keyPresses = []
        for event in events:
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: self.keys[0] = True
                elif event.key == pygame.K_LEFT: self.keys[1] = True
                elif event.key == pygame.K_DOWN: self.keys[2] = True
                elif event.key == pygame.K_RIGHT: self.keys[3] = True
                elif event.key == pygame.K_SPACE: self.keys[4] = True
                elif event.key == pygame.K_w: self.keys[0] = True
                elif event.key == pygame.K_a: self.keys[1] = True
                elif event.key == pygame.K_s: self.keys[2] = True
                elif event.key == pygame.K_d: self.keys[3] = True
                elif event.key == pygame.K_SPACE: self.keys[4] = True
                elif event.key == pygame.K_LSHIFT: self.keys[5] = True
                elif event.key == pygame.K_RETURN: self.keyPresses.append(pygame.K_RETURN)
                elif event.key == pygame.K_BACKSPACE:
                    self.keyPresses.append(pygame.K_BACKSPACE)
                if not (event.key == pygame.K_BACKSPACE or event.key == pygame.K_RETURN):
                    self.keyPresses.append(event.unicode)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP: self.keys[0] = False
                elif event.key == pygame.K_LEFT: self.keys[1] = False
                elif event.key == pygame.K_DOWN: self.keys[2] = False
                elif event.key == pygame.K_RIGHT: self.keys[3] = False
                elif event.key == pygame.K_w: self.keys[0] = False
                elif event.key == pygame.K_a: self.keys[1] = False
                elif event.key == pygame.K_s: self.keys[2] = False
                elif event.key == pygame.K_d: self.keys[3] = False
                elif event.key == pygame.K_SPACE: self.keys[4] = False
                elif event.key == pygame.K_LSHIFT: self.keys[5] = False


            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 1:self.keys[4] = True#x = Space
                if event.button == 2:self.keys[5] = True#O = shift
                if event.button == 7:self.keys[4] = True#R2 = Space
                if event.button == 6:self.keys[5] = True#L2 = Shift
                if event.button == 0:self.keyPresses.append(pygame.K_RETURN)
            elif event.type == pygame.JOYBUTTONUP:
                if event.button == 1:self.keys[4] = False
                if event.button == 2:self.keys[5] = False
                if event.button == 7:self.keys[4] = False
                if event.button == 6:self.keys[5] = False


            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.keyPresses.append("MouseButton")
                    self.keys[6] = True
                if event.button == 3:
                    self.keyPresses.append("RightClick")
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.keys[6] = False
            elif event.type == pygame.VIDEORESIZE:
                self.width, self.height = event.size
                self.setWindow()
                self.level()
        self.mx, self.my = pygame.mouse.get_pos()
        self.time = time.time()
        for object in self.objects:
            object.tick()
        for object in self.menuElements:
            if object.exists: object.tick()
        self.lastTime = self.time
    def render(self):
        self.win.fill(self.backGroundColor)
        for object in self.objects:
            object.render()
        for object in self.menuElements:
            if object.exists: object.render()
        pygame.display.update()
    def level(self):
        self.menuElements = [Label(self.width - 200, 10, ""), Button(10,10, "Menu", width = 100)]
        self.fpsUpdate()
    def deinit(self):
        pygame.quit()

class Object:
    def __init__(self):
        self.x, self.y = 0,0
        self.type = None
        self.exists = True
        self.num = 0
    def tick(self):
        pass
    def render(self):
        pass
class Button:
    def __init__(self, x,y, text, exists = True, width = 100, height = 50, num = -1, color = (128, 128, 128), hoverColor = (255,255,255), textColor = (0,0,0), textHoverColor = (0,0,0)):
        self.type = "Button"
        self.x, self.y = x,y
        self.exists = exists
        self.text = text
        self.width, self.height = width, height
        self.color, self.hoverColor = color, hoverColor
        self.textColor, self.textHoverColor = textColor, textHoverColor
        self.hover = False
        self.num = num
    def checkHover(self, mx, my):
        if mx >= self.x and mx <= self.x+self.width and my >= self.y and my <= self.y+self.height:
            return True
        return False
    def tick(self):
        self.hover = self.checkHover(game.mx, game.my)
        if "MouseButton" in game.keyPresses and self.hover:
            game.keyPresses.remove("MouseButton")
            self.action()
    def render(self):
        if self.hover:
            pygame.draw.rect(game.win, self.hoverColor, (self.x, self.y, self.width, self.height))
            text = game.font.render(self.text, True, self.textHoverColor)
            game.win.blit(text, (self.x+(self.width-text.get_width())//2, self.y+5))
        else:
            pygame.draw.rect(game.win, self.color, (self.x, self.y, self.width, self.height))
            text = game.font.render(self.text, True, self.textColor)#optimize by rendering seperately from frames
            game.win.blit(text, (self.x+(self.width-text.get_width())//2, self.y+5))
    def action(self):
        if self.text == "Quit Game":
            game.run = False
            return
        elif self.text == "Menu":
            game.currentStage = -1
            game.level()
            return
class Clicker:
    def __init__(self, clicks, action):
        self.type = "Clicker"
        self.clicks = clicks
        self.hover = False
        self.hoverObject = None
        self.action = action
        self.exists = True
    def tick(self):
        self.hover = False
        self.hoverObject = None
        for click in self.clicks:
            if((game.mx-click.x)**2+(game.my-click.y)**2)**0.5 < 50:
                self.hover = True
                self.hoverObject = click
                if "MouseButton" in game.keyPresses:
                    if self.action == "Remove an Object":
                        if game.goal > game.createObjects.index(click):
                            game.goal -= 1
                        game.createObjects.remove(click)
                        print(click)
                        print(game.objects)
                    else:
                        game.goal = max(1,game.createObjects.index(click))
                        click.size = 50
                        click.color = (255,0,0)
                    game.currentStage = -2
                    game.level()
    def render(self):
        if self.hover:
            pygame.draw.circle(game.win, (128,128,128), (int(self.hoverObject.x), int(self.hoverObject.y)), 50)
class Dart:
    def __init__(self, throw):
        self.throw = throw
        self.type = "Dart"
        self.exists = True
    def tick(self):
        #self.throw.x, self.throw.y = game.mx, game.my
        if "MouseButton" in game.keyPresses:
           self.throw.startX, self.throw.startY = game.mx, game.my
           game.keyPresses.remove("MouseButton")
           self.action()
    def action(self):
           if self.throw.type == "Sun":
               game.currentStage = -6
               game.level()
           else:
               game.currentStage = -5
               game.level()
    def render(self):
        self.throw.x, self.throw.y = game.mx, game.my
class Arrow:
    def __init__(self, start):
        self.start = start
        self.type = "Arrow"
        self.exists = True
        self.x, self.y = game.mx, game.my
    def tick(self):
        self.x, self.y = game.mx, game.my
        factor = 0.01
        self.start.startXVel, self.start.startYVel = (game.mx-self.start.x)*factor, (game.my-self.start.y)*factor
        self.start.xVel, self.start.yVel = self.start.startXVel, self.start.startYVel
        if "MouseButton" in game.keyPresses:
            game.keyPresses.remove("MouseButton")
            self.start.reset()
            if self.start.type == "Player":
                game.currentStage = -2
                game.level()
            else:
                game.currentStage = -6
                game.level()
        elif "RightClick" in game.keyPresses:
            game.keyPresses.remove("RightClick")
            factor = 0.01
            self.start.startXVel, self.start.startYVel = 0,0
            self.start.reset()
            if self.start.type == "Player":
                game.currentStage = -2
                game.level()
            else:
                game.currentStage = -6
                game.level()
    def render(self):
        pygame.draw.line(game.win, (255,255,255), (self.start.x, self.start.y), (self.x, self.y), 3)
class Weight:
    def __init__(self, obj):
        self.type = "Weight"
        self.exists = True
        self.obj = obj
        self.x, self.y = game.mx, game.my
        self.radius = 0
    def tick(self):
        self.x, self.y = game.mx, game.my
        self.radius = ((self.x-self.obj.x)**2+(self.y-self.obj.y)**2)**0.5
        factor = 10
        self.obj.gravity = self.radius*factor
        if "MouseButton" in game.keyPresses:
            game.keyPresses.remove("MouseButton")
            game.currentStage = -2
            game.level()
        elif "RightClick" in game.keyPresses:
            game.keyPresses.remove("RightClick")
            factor = 10
            self.obj.gravity = 0
            game.currentStage = -2
            game.level()
    def render(self):
        pygame.draw.circle(game.win, (128,128,128), (self.obj.x, self.obj.y), int(self.radius))
class Label:
    def __init__(self, x,y, text, exists = True, bound = None, center = "L"):
        self.type = "Label"
        self.startX, self.startY = x,y
        self.x, self.y = x,y
        self.text = text
        self.exists = exists
        self.bound = bound
        self.color = (255,255,255)
        self.drawn = False
        self.center = center
        self.paint()
    def paint(self):
        self.font = game.font.render(self.text, True, self.color)
    def tick(self):
        if self.bound != None:
            self.x, self.y = self.bound.x+self.startX, self.bound.y+self.startY
    def render(self):
        if self.center == "L": x = self.x+10
        elif self.center == "M": x = self.x - self.font.get_width()//2
        elif self.center == "R": x = self.x - self.font.get_width()-10
        game.win.blit(self.font, (x, self.y+5))
        self.drawn = True
        
class TextBox:
    def __init__(self, x,y, width, height,  exists = True, startText = "Username", textCache = "", num = 0):
        self.type = "TextBox"
        self.x, self.y = x,y
        self.width, self.height = width, height
        self.activeColor = (255,255,255)
        self.inactiveColor = (128, 128, 128)
        self.active = False
        self.exists = exists
        self.text = self.startText = startText
        self.num = num
        if len(game.textCaches) > self.num:
            if game.textCaches[num] != "":
                self.text = game.textCaches[num]
        else: game.textCaches.append("")

    def tick(self):
        if "MouseButton" in game.keyPresses:
            if game.mx >= self.x and game.mx <= self.x+self.width and game.my >= self.y and game.my <= self.y+self.height:
                self.active = True
                if self.text == self.startText: self.text = ""
            else:
                self.active = False
                if self.text == "": self.text = self.startText
        if self.active:
            for key in game.keyPresses:
                if key == pygame.K_RETURN:
                    self.action()
                    self.active = False
                elif key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    game.textCaches[self.num] = self.text
                elif key != "MouseButton":
                    self.text+=key
                    game.textCaches[self.num] = self.text
    def render(self):
        text = game.font.render(self.text, True, (0,0,0))
        if self.active:
            pygame.draw.rect(game.win, self.activeColor, (self.x, self.y, self.width, self.height))
            if round(time.time()*1.3)%2 == 0:
                pygame.draw.line(game.win, (0,0,0), (self.x+(self.width+text.get_width())//2, self.y+10), (self.x+(self.width+text.get_width())//2, self.y+40),2)
        else: pygame.draw.rect(game.win, self.inactiveColor, (self.x, self.y, self.width, self.height))
        game.win.blit(text, (self.x+(self.width-text.get_width())//2, self.y+5))
    def action(self):
        pass
class Line(Object):
    def __init__(self, x1,y1, x2,y2, color = (255,255,255), width = 5):
        super().__init__()
        self.x1, self.y1, self.x2, self.y2 = x1,y1,x2,y2
        self.color = color
        self.width = width
        self.exists = True
    def tick(self):
        pass
    def render(self):
        pygame.draw.line(game.win, self.color, (self.x1,self.y1),(self.x2,self.y2), self.width)
class Image(Object):
    def __init__(self, x,y, width, height, image, rotation = 0, center = "TopLeft"):
        self.exists = True
        self.type = "Image"
        self.x, self.y = x,y
        self.width, self.height = width, height
        self.rotation = rotation
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.center = center
    def tick(self):
        pass
    def render(self):
        rotated = pygame.transform.rotate(self.image, self.rotation)
        x,y = (self.x-game.width//2)*game.zoom + game.width//2, (self.y-game.height//2)*game.zoom + game.height//2
        if self.center == "TopLeft":
            game.win.blit(rotated, (x,y))
        elif self.center == "Center":
            shift = rotated.get_rect()
            game.win.blit(rotated, (x-shift.center[0], y-shift.center[1]))

        #game.win.blit(pygame.transform.rotate(self.image, self.rotation), (self.x,self.y))
class Group(Object):
    def __init__(self, x,y, width, height):
        self.objects = []
        self.menuElements = []
        self.x, self.y = x,y
        self.width, self.height = width, height
    def tick(self):
        for object in self.objects:
            object.tick()
        for object in self.menuElements:
            if object.exists: object.tick()
    def render(self):
        for object in self.objects:
            object.render()
        for object in self.menuElements:
            if object.exists: object.render()

class rectangle(Object):
    def __init__(self, x,y, width, height, color):
        self.type = "Rectangle"
        pass
    def tick(self):
        pass
    def render(self):
        pass


def userInputFPS(valid = True):
    if valid == True: a = input("\nUnable to detect display Frequency.\n\nPress 'Enter' to set FPS to 60 (default)\nenter a number to set custom framerate: ")
    else: a = input(valid+" is an invalid Framerate.\nPlease enter a valid Framerate or press Enter to skip.")
    if a == "": return 60
    else:
        try:
            if int(a) >= 20 and int(a) <= 360:
                return int(a)
            else: return userInputFPS(a)
        except: return userInputFPS(a)
#tick per second
tps = 144
#change per tick
cpt = 0.02
#fps
def getFPS():
    try:
        import win32api
        fps = getattr(win32api.EnumDisplaySettings(win32api.EnumDisplayDevices().DeviceName, -1), "DisplayFrequency")
        if fps==59: fps = 60
    except: fps = userInputFPS()
    return fps

def Main(game):
    game.level()

    now = nowTime = time.time()
    last, lastTime = now, now
    tCount, fCount = 0,0
    tickDelta, frameDelta = 0,0
    sleepTime = 1/game.tps/10

    while game.run:
        now = nowTime = time.time()
        tickDelta += (now-last)/game.tickTime
        frameDelta += (now-last)/game.frameTime
        last = now
        while tickDelta >= 1:
            events = pygame.event.get()
            game.tick(events)
            tickDelta -= 1
            tCount += 1
        if frameDelta >= 1:
            game.render()
            frameDelta -= math.floor(frameDelta)
            fCount += 1
        if nowTime >= lastTime + 1:
            game.FPS, game.TPS = fCount, tCount
            game.fpsUpdate()
            lastTime = now
            if fCount >= 3/4*1/game.frameTime and tCount >= 0.9*1/game.tickTime:
                sleepTime = 1/game.tps/10
            else:
                sleepTime = 0

            fCount, tCount = 0,0

        time.sleep(sleepTime)
    game.deinit()
