import time, math, random, os
from game import *

os.environ['SDL_VIDEO_CENTERED'] = '1'

class Game(Game):
    def __init__(self, width, height, fps, tps):

        #initializers
        super().__init__(width, height, fps, tps)
        self.stages = []
        self.createObjects = []
        self.static = True
        self.run = True
        #zoom
        self.xDist, self.yDist = 0,0
        #username
        self.player = -1
        #paths
        self.docPath = "data/docs/"
        self.imagePath = "data/images/"
        self.highscoreFile = "fastest.txt"
        self.efficientFile = "cleanest.txt"
        #highscores
        self.boostTime = 0
        self.beginTime = 0
        self.highscores = []
        self.efficient = []
        self.scroll = 0
        #upgrades
        self.boostStrength = 0.005
        self.sideBoosters = 0
        self.boostType = 0
        #settings
        self.trail = False
        self.showFPS = True
        self.showHighscores = False
        self.showTimes = False
        self.showFuture = False
        self.showForceVector = False
        #copyrights
        self.rocketNames = ["Saturn I", "SpaceX Starship", "Saturn V", "Falcon Heavy"]
        self.rocketImages = [pygame.image.load(self.imagePath+"rocket"+str(i+1)+".png") for i in range(len(self.rocketNames))]
        self.rocketBoostImages = [pygame.image.load(self.imagePath+"rocket"+str(i+1)+"_boost.png") for i in range(len(self.rocketNames))]
        #init
        self.loadHighscores()
        self.loadLevels()
    def windowUpdate(self):
        self.xViewRadius = self.width//2
        self.yViewRadius = self.height//2
    def tick(self, events):
        super().tick(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.move = not self.move
        self.zoom = 1
        while self.xDist > self.xViewRadius or self.yDist > self.yViewRadius:
            self.xDist *= 0.5
            self.yDist *= 0.5
            self.zoom *= 0.5
        self.checkComplete()
    def update(self):
       self.win.fill(self.backGroundColor)
    def render(self):
        self.win.fill(self.backGroundColor)
        for object in self.objects:
            object.render()
        for object in self.menuElements:
            if object.exists: object.render()
        pygame.display.update()
    def loadLevels(self):
        self.stages = []
        self.readLevels(self.docPath+"levels.txt")
        self.readLevels(self.docPath+"test.txt")
    def readLevels(self, file):
        f = open(file, "r")
        lines = f.readlines()
        stages = [[]]
        stage = 0
        for l in lines:
            if l == "\n":
                stage += 1
                stages.append([])
            elif stage < len(lines):
                object = l.replace("\n", "").split(" ")
                for i in range(len(object)):
                    if object[i] == "True" or object[i] == "False":
                        value = False
                    else:
                        try: value = int(object[i])
                        except:
                            try: value = float(object[i])
                            except: value = object[i]
                    object[i] = value
                stages[stage].append(object)
        self.stages += stages
    def writeLevels(self):
        ready = True
        for i in range(len(self.createObjects)):
            if self.createObjects[i].type == "Player" and False:
                self.createObjects.insert(0,self.createObjects.pop(i))
                ready = True
        if ready:
            f = open(self.docPath+"test.txt", "a")
            f.write("\n\n")
            for obj in self.createObjects:
                if obj.type == "Player":
                    f.write("player"+" "+str(obj.startX)+" "+str(obj.startY)+" "+str(random.randint(1,4))+" "+str(obj.startXVel)+" "+str(obj.startYVel)+" "+str(0)+"\n")
                if obj.type == "Sun":
                    f.write("sun"+" "+str(obj.startX)+" "+str(obj.startY)+" "+str(obj.gravity)+"\n")
                if obj.type == "Planet":
                    f.write("planet"+" "+str(obj.startX)+" "+str(obj.startY)+" "+str(obj.startXVel)+" "+str(obj.startYVel)+" "+str(obj.gravity)+"\n")
            f.write(str(self.goal)+" "+"50"+" "+self.username)
            f.close()
            f = open(self.highscoreFile,"a")
            f.write("- Noone\n")
            f.close()
            f = open(self.efficientFile,"a")
            f.write("- Noone\n")
            f.close()
    def loadHighscores(self):
        f = open(self.docPath+self.highscoreFile, "r")
        highscores = f.readlines()
        for i in range(len(highscores)):
            highscores[i] = highscores[i].replace("\n", "").split(" ")
        self.highscores = highscores
        f = open(self.docPath+self.efficientFile, "r")
        highscores = f.readlines()
        for i in range(len(highscores)):
            highscores[i] = highscores[i].replace("\n", "").split(" ")
        self.efficient = highscores
    def writeHighscores(self, fast):
        f = open((self.docPath+self.efficientFile) if fast else (self.docPath+self.efficientFile), "w")
        highscores = []
        for h in self.highscores if fast else self.efficient:
            highscores.append(str(h[0])+" "+h[1]+"\n")
        f.writelines(highscores)
        f.close()
    def level(self):
        self.setFrameRate(20,20)
        super().level()
        self.player = -1
        self.move = False

        if False:
            pass
        elif self.currentStage == -10:
            #workshop menu
            #, Saturn I, SpsceX Starship, Saturn V, Falcon Heavy
            for i in range(len(self.rocketNames)):
                self.menuElements.append(Button(self.width//2-len(self.rocketNames)*100+200*i, self.height//2-150, self.rocketNames[i], width = 200))
                self.menuElements.append(Image(self.width//2-len(self.rocketNames)*100+200*i+10, self.height//2-50, 180,400, self.rocketImages[i]))
            self.menuElements.append(Label(self.width//2 - 100, self.height//2-300, "Select your rocket"))
        elif self.currentStage == -9:
            #settings menu
            width = 250
            self.menuElements.append(Button(self.width//2-width, self.height//2-200, "Trail", width = width))
            self.menuElements.append(Label(self.width//2 + 10, self.height//2-200, "ON" if self.trail else "OFF"))
            self.menuElements.append(Button(self.width//2-width, self.height//2-140, "Show FPS", width = width))
            self.menuElements.append(Label(self.width//2 + 10, self.height//2-140, "ON" if self.showFPS else "OFF"))
            self.menuElements.append(Button(self.width//2-width, self.height//2-80, "Show Highscores", width = width))
            self.menuElements.append(Label(self.width//2 + 10, self.height//2-80, "ON" if self.showHighscores else "OFF"))
            self.menuElements.append(Button(self.width//2-width, self.height//2-20, "Show Times", width = width))
            self.menuElements.append(Label(self.width//2 + 10, self.height//2-20, "ON" if self.showTimes else "OFF"))
            self.menuElements.append(Button(self.width//2-width, self.height//2+40, "Show Future", width = width))
            self.menuElements.append(Label(self.width//2 + 10, self.height//2+40, "ON" if self.showFuture else "OFF"))
            self.menuElements.append(Button(self.width//2-width, self.height//2+100, "Show Force Vector", width = width))
            self.menuElements.append(Label(self.width//2 + 10, self.height//2+100, "ON" if self.showForceVector else "OFF"))
        elif self.currentStage == -8:
            #highscorelist
            self.loadHighscores()
            self.menuElements.append(Button(10,self.height//2-55, "Up"))
            self.menuElements.append(Button(10,self.height//2+5, "Down"))
            self.menuElements.append(Label(self.width//2 - 280, 100, "Fastest:"))
            self.menuElements.append(Label(self.width//2 + 300, 100, "Least Fuel:"))
            for i in range(len(self.highscores)):
                k = i+game.scroll
                if k >= 0 and k < len(self.highscores) and 210+50*k < game.height:
                    self.menuElements.append(Label(self.width//2 - 640, 160+50*k, "Level "+str(i)+":"))
                    self.menuElements.append(Label(self.width//2 - 280, 160+50*k, self.highscores[i][1]))
                    self.menuElements.append(Label(self.width//2 - 100, 160+50*k, str(self.highscores[i][0])+"s"))
                    self.menuElements.append(Label(self.width//2 + 300, 160+50*k, self.efficient[i][1]))
                    self.menuElements.append(Label(self.width//2 + 500, 160+50*k, str(self.efficient[i][0])+"s"))
        elif self.currentStage == -7:
            #select object menu
            self.tickTime, self.frameTime = 1/self.tps, 1/self.fps
            self.objects = self.createObjects
            self.menuElements.append(Button(10,70, "Back"))
        elif self.currentStage == -6:
            #gravity menu
            self.tickTime, self.frameTime = 1/self.tps, 1/self.fps
            self.objects = self.createObjects
            self.menuElements.append(Weight(self.objects[-1]))
        elif self.currentStage == -5:
            #velocity menu
            self.tickTime, self.frameTime = 1/self.tps, 1/self.fps
            self.objects = self.createObjects
            self.menuElements.append(Arrow(self.objects[-1]))
        elif self.currentStage == -4:
            #drag object menu
            self.tickTime, self.frameTime = 1/self.tps, 1/self.fps
            self.objects = self.createObjects
            self.menuElements.append(Dart(self.objects[-1]))
        elif self.currentStage == -3:
            #level select menu
            self.loadLevels()
            stack = self.height//50 - 2
            stack = self.height//50 - 2
            for i in range(len(self.stages)):
                self.menuElements.append(Button(10+130*(i//stack),70+50*(i%stack),"Stage "+str(i), width = 120))
        elif self.currentStage == -2:
            #create menu
            self.setFrameRate(self.fps, self.tps)
            self.menuElements.append(Button(10,70, "Sun", width = 100))
            self.menuElements.append(Button(10,120, "Planet", width = 100))
            self.menuElements.append(Button(10,170, "Player", width = 100))
            self.menuElements.append(Button(10,230, "Remove an Object", width = 250))
            self.menuElements.append(Button(10,280, "Choose the target", width = 250))
            self.menuElements.append(Button(10,340, "Save Stage", width = 150))
            self.menuElements.append(Button(10,390, "Undo", width = 150))
            self.menuElements.append(Button(10,440, "Reset", width = 150))
            self.objects = self.createObjects
            self.goal = -1
        elif self.currentStage == -1:
            #main menu
            self.objects = []
            self.menuElements.append(Button(self.width//2 -75, self.height//2 - 75,"Start Game", width = 150))
            self.menuElements.append(Button(self.width//2 -75, self.height//2 - 25,"Play Stage", width = 150))
            self.menuElements.append(Button(self.width//2 -100, self.height//2 + 35,"Create Stage", width = 200))
            self.menuElements.append(Button(self.width//2 -100, self.height//2 + 85,"Highscores", width = 200))
            self.menuElements.append(TextBox(self.width//2-100, self.height//2 + 145, 200, 50))
            self.menuElements.append(Button(10, self.height - 170, "Workshop", width = 150))
            self.menuElements.append(Button(10, self.height - 110, "Settings", width = 150))
        else:
            #level stage
            self.objects = []
            self.move = True
            self.setFrameRate(self.fps, self.tps)
            self.move = True
            self.boostTime = 0
            self.beginTime = time.time()
            self.loadHighscores()
            defaultStages = 0
            if self.currentStage - defaultStages < len(self.stages):
                s = self.stages[self.currentStage - defaultStages]
                for i in range(len(s)):
                    object = s[i]
                    if object[0] == "player":
                        self.objects.append(Player(object[1], object[2], object[3], object[4], object[5], object[6]))
                        self.player = i
                    elif object[0] == "planet": self.objects.append(Planet(object[1], object[2], object[3], object[4], object[5]))
                    elif object[0] == "sun":
                        if len(object) == 4: self.objects.append(Sun(object[1], object[2], object[3], True))
                        else: self.objects.append(Sun(object[1], object[2], object[3], object[4]))
                    else:
                        self.goal = int(object[0])
                        self.objects[self.goal].color = (255,0,0)
                        self.range = object[1]
                        self.objects[self.goal].size = object[1]
                        if len(object) == 3:
                            self.objects.append(Label(110, 60, "Created by "+object[2]))
                self.menuElements.append(Label(110, 10, "Level "+str(self.currentStage)))

                self.menuElements.append(Label(400, 50, "Press 'Left_Shift' to slow down!", self.currentStage == 1))
                self.menuElements.append(Label(400, 150, "Press 'Return' to restart the stage!", self.currentStage == 1))
                self.menuElements.append(Label(400, 50, "Leave the star's orbit and fly to the red target!", self.currentStage == 2))

                high1 = self.highscores[self.currentStage]
                high2 = self.efficient[self.currentStage]

                self.menuElements.append(Label(-20, -50, self.username if self.username != "Guest" else "You", self.currentStage == 0, self.objects[0]))
                self.menuElements.append(Label(400, 50, "Press 'Space' to accelerate", self.currentStage == 0))
                self.menuElements.append(Label(self.width-250, 70, "Fastest:", self.showHighscores))
                self.menuElements.append(Label(self.width-250, 120, str(high1[1])+" - "+str(high1[0])+"s", self.showHighscores))
                self.menuElements.append(Label(self.width-250, 170, "Least Fuel:", self.showHighscores))
                self.menuElements.append(Label(self.width-250, 220, str(high2[1])+" - "+str(high2[0])+"s", self.showHighscores))
                self.menuElements.append(Label(self.width-250, self.height-120, "Time: "+str(0), self.showTimes))
                self.menuElements.append(Label(self.width-250, self.height-60, "Boost: "+str(0), self.showTimes))

            else:
                print("Congratulations, you've won the game!")
                self.currentStage = -1
                self.level()

    def drawArrow(self, x1,y1, xAcc, yAcc):
        width = 3
        length = .4
        tipLength = 10
        
        x2,y2 = x1 + xAcc  * length, y1 + yAcc * length
        x, y = x2-x1, y2-y1
        dist = (x**2 + y**2)**.5
        pygame.draw.line(self.win, (255,255,255), (x1,y1), (x2, y2), width)
        
        if x != 0 and y != 0:
            vector = x/dist, y/dist
            vector1 = -vector[1], vector[0]
            pygame.draw.line(self.win, (255,255,255), (x2, y2), (x2 - (vector[0]+vector1[0])*tipLength, y2-(vector[1]+vector1[1])*tipLength), width)
            pygame.draw.line(self.win, (255,255,255), (x2, y2), (x2 - (vector[0]-vector1[0])*tipLength, y2-(vector[1]-vector1[1])*tipLength), width)

    def checkComplete(self):
        if self.player >= 0:
            x = self.objects[self.player].x - self.objects[self.goal].x
            y = self.objects[self.player].y - self.objects[self.goal].y
            if (x**2+y**2)**0.5 <= self.range:
                if self.highscores[self.currentStage][0] == "-" or float(self.highscores[self.currentStage][0]) > time.time()-self.beginTime:
                    self.highscores[self.currentStage] = [round(time.time()-self.beginTime, 3), self.username]
                    self.writeHighscores(True)
                if self.efficient[self.currentStage][0] == "-" or float(self.efficient[self.currentStage][0]) > self.boostTime:
                    self.efficient[self.currentStage] = [round(self.boostTime, 3), self.username]
                    self.writeHighscores(False)
                self.currentStage += 1
                self.level()
        else: return False

class Button(Button):
    def action(self):
        super().action()
        if self.text == "Create Stage" or self.text == "Back":
            game.currentStage = -2
            game.level()
        elif self.text == "Start Game":
            game.currentStage = 0
            game.level()
        elif self.text == "Play Stage":
            game.currentStage = -3
            game.level()
        elif self.text == "Sun":
            game.currentStage = -4
            game.createObjects.append(Sun(game.mx,game.my,500))
            game.level()
        elif self.text == "Planet":
            game.currentStage = -4
            game.createObjects.append(Planet(game.mx, game.my, 0, 0, 250))
            game.level()
        elif self.text == "Player":
            game.currentStage = -4
            game.createObjects.append(Player(game.mx, game.my, 1, 0, 0, 0))
            game.level()
        elif self.text == "Choose the target":
            game.currentStage = -7
            game.level()
            game.menuElements.append(Clicker(game.createObjects, self.text))
        elif self.text == "Remove an Object":
            game.currentStage = -7
            game.level()
            game.menuElements.append(Clicker(game.createObjects, self.text))
        elif self.text == "Save Stage":
            game.writeLevels()
        elif self.text == "Reset":
            game.createObjects = []
            game.level()
        elif self.text == "Undo":
            if len(game.createObjects) > 0:
                game.createObjects.pop(-1)
                game.level()
        elif self.text == "Highscores":
            game.currentStage = -8
            game.level()
        elif self.text == "Down":
            game.scroll -= 5
            game.level()
        elif self.text == "Up":
            game.scroll += 5
            game.level()
        elif self.text == "Settings":
            game.currentStage = -9
            game.level()
        elif self.text == "Trail":
            game.trail = not game.trail
            game.level()
        elif self.text == "Show FPS":
            game.showFPS = not game.showFPS
            game.level()
        elif self.text == "Show Highscores":
            game.showHighscores = not game.showHighscores
            game.level()
        elif self.text == "Show Times":
            game.showTimes = not game.showTimes
            game.level()
        elif self.text == "Show Future":
            game.showFuture = not game.showFuture
            game.level()
        elif self.text == "Show Force Vector":
            game.showForceVector = not game.showForceVector
            game.level()
        elif self.text == "Workshop":
            game.currentStage = -10
            game.level()
        else:
            for i in range(len(game.rocketNames)):
                if self.text == game.rocketNames[i]:
                    game.boostType = i
                    for j in range(len(game.rocketNames)):
                        game.menuElements[j*2+2].height = 50
                        game.menuElements[j*2+2].hoverColor = (255,255,255)
                    self.height = 450
                    self.hoverColor = (128,128,128)
            for i in range(len(game.stages)):
                if self.text == "Stage "+str(i):
                    game.currentStage = i
                    game.level()
                    break
class TextBox(TextBox):
    def action(self):
        if self.num == 0:
            game.username = self.text


class Player(object):
    def __init__(self, x,y, boostType, xVel, yVel, gravity):
        self.startX, self.startY = x,y
        self.startXVel, self.startYVel = xVel, yVel
        self.fakeX, self.fakeY = x,y
        self.fakeXVel, self.fakeYVel = xVel, yVel
        self.speed = game.sideBoosters
        self.boost = game.boostStrength
        self.size = 3
        self.color = (255,255,255)
        self.reset()
        self.gravity = gravity
        self.booster = False
        self.boostType = game.boostType
        self.type = "Player"
        self.traillength = 5000 if game.trail else 0
        self.boostImage = image = game.rocketBoostImages[self.boostType]
        self.image = game.rocketImages[self.boostType]
        self.prerenders = []
        self.predicts = 1000
    def reset(self):
        self.trail = []
        self.x, self.y = self.startX,self.startY
        self.xVel, self.yVel = self.startXVel, self.startYVel
        self.xAcc, self.yAcc = 0,0
        game.beginTime = time.time()
        game.boostTime = 0
        #game.objects[-2].text = "Boost: "+str(round(game.boostTime,3))
    def tick(self):
        if game.move:
            self.xAcc, self.yAcc = 0,0
            if game.keys[0]: self.yAcc -= self.speed
            if game.keys[1]: self.xAcc -= self.speed
            if game.keys[2]: self.yAcc += self.speed
            if game.keys[3]: self.xAcc += self.speed
            if game.keys[4]:
                try:
                    share = ((self.xVel**2+self.yVel**2)**0.5+self.boost)/(self.xVel**2+self.yVel**2)**0.5
                    self.xVel *= share
                    self.yVel *= share
                    self.booster = True
                except:
                    self.xVel += self.boost
                game.boostTime += game.time - game.lastTime
                if game.showTimes:
                    game.menuElements[-1].text = "Boost: "+str(round(game.boostTime,3))
                    game.menuElements[-1].paint()
            else: self.booster = False
            if game.keys[5]:
                try: share = ((self.xVel**2+self.yVel**2)**0.5-self.boost)/((self.xVel**2+self.yVel**2)**0.5)
                except: share = 1
                self.xVel *= share
                self.yVel *= share
                game.boostTime += game.time - game.lastTime
                if game.showTimes:
                    game.menuElements[-2].text = "Boost: "+str(round(game.boostTime,3))
                    game.menuElements[-2].paint()
            if game.showTimes and game.currentStage >= 0:
                game.menuElements[-2].text = "Time: "+str(round(game.time-game.beginTime,3))
                game.menuElements[-2].paint()
            self.trail.append((int(self.x), int(self.y)))
            if len(self.trail) > self.traillength:
                self.trail = self.trail[1:]

            for g in game.objects:
                if g != self:
                    try:
                        self.xAcc -=  g.gravity * (self.x-g.x)/((self.x-g.x)**2+(self.y-g.y)**2)**1.5
                        self.yAcc -= g.gravity * (self.y-g.y)/((self.x-g.x)**2+(self.y-g.y)**2)**1.5
                    except: pass
            self.xVel += self.xAcc
            self.yVel += self.yAcc
            self.x += self.xVel
            self.y += self.yVel
            borders = False
            if borders:
                if self.x > game.width - self.width:
                    self.x, self.xVel = game.width-self.width, 0
                if self.x < 0:
                    self.x, self.xVel = 0,0
                if self.y > game.height - self.height:
                    self.y, self.yVel = game.height-self.height, 0
                if self.y < 0:
                    self.y, self.yVel = 0,0
        game.xDist, game.yDist = ((self.x-960)**2)**0.5, ((self.y-500)**2)**0.5
        if pygame.K_RETURN in game.keyPresses: self.reset()
    def render(self):
        if self.xVel == self.yVel == 0: angle = -90
        else: angle = 180+math.atan2(self.xVel,self.yVel)*180/math.pi
        if self.booster: image = self.boostImage
        else: image = self.image
        scale = 0.17*game.zoom
        image = pygame.transform.scale(image, (int(max(1,image.get_rect()[2]*scale)), int(max(1,image.get_rect()[3]*scale))))
        rotated = pygame.transform.rotate(image, angle)
        shift = rotated.get_rect()
        x,y = (self.x-game.width//2)*game.zoom + game.width//2, (self.y-game.height//2)*game.zoom + game.height//2
        step = max(1,len(self.trail)//500)
        if game.showFuture:
            self.fake()
        for i in range(0,len(self.trail)-step,step):
            pygame.draw.line(game.win, (255,0,0), (int((self.trail[i][0]-game.width//2)*game.zoom+game.width//2), int((self.trail[i][1]-game.height//2)*game.zoom+game.height//2)), (int((self.trail[i+step][0]-game.width//2)*game.zoom+game.width//2), int((self.trail[i+step][1]-game.height//2)*game.zoom+game.height//2)), 2)
        #pygame.draw.circle(game.win, (self.color), (int(x), int(y)), self.size)
        if game.showForceVector: game.drawArrow(x,y, self.xAcc*10000, self.yAcc*10000)
        game.win.blit(rotated, (int(x-shift.center[0]), int(y-shift.center[1])))
    def fake(self):
        step = max(1,self.predicts//200)
        self.prerenders = [(self.x,self.y,self.xVel, self.yVel)]
        for g in game.objects:
            if g.type == "Planet" or g.type == "Player":
                g.fakeX, g.fakeY = g.x,g.y
                g.fakeXVel, g.fakeYVel = g.xVel, g.yVel
                g.prerenders = [(g.x,g.y,g.xVel, g.yVel)]
        for i in range(self.predicts):
            for g in game.objects:
                if g.type == "Planet" or g.type == "Player":
                    g.fakeTick()
        if True:
            for obj in game.objects:
                if obj.type == "Player" or obj.type == "Planet":
                    if obj.type == "Player": color = (255,255,255)
                    else: color = (50,50,255)
                    for i in range(0,len(obj.prerenders)-step,step):
                        pygame.draw.line(game.win, color, (int((obj.prerenders[i][0]-game.width//2)*game.zoom+game.width//2), int((obj.prerenders[i][1]-game.height//2)*game.zoom+game.height//2)), (int((obj.prerenders[i+step][0]-game.width//2)*game.zoom+game.width//2), int((obj.prerenders[i+step][1]-game.height//2)*game.zoom+game.height//2)), 2)

    def fakeTick(self):
        for g in game.objects:
                if g != self:
                    try:
                        if g.type == "Sun":
                            if g.gravity != 0:
                                self.fakeXVel -= g.gravity * (self.fakeX-g.x)/((self.fakeX-g.x)**2+(self.fakeY-g.y)**2)**1.5
                                self.fakeYVel -= g.gravity * (self.fakeY-g.y)/((self.fakeX-g.x)**2+(self.fakeY-g.y)**2)**1.5
                        elif g.type == "Planet":
                            if g.gravity != 0:
                                self.fakeXVel -= g.gravity * (self.fakeX-g.fakeX)/((self.fakeX-g.fakeX)**2+(self.fakeY-g.fakeY)**2)**1.5
                                self.fakeYVel -= g.gravity * (self.fakeY-g.fakeY)/((self.fakeX-g.fakeX)**2+(self.fakeY-g.fakeY)**2)**1.5
                    except:
                        print("error")
        self.fakeX += self.fakeXVel
        self.fakeY += self.fakeYVel
        self.prerenders.append((self.fakeX,self.fakeY,self.fakeXVel, self.fakeYVel))
class Sun(object):
    def __init__(self, x,y, gravity, visible = True):
        self.x, self.y = x,y
        self.gravity = gravity
        self.size = 10
        self.color = (255,255,0)
        self.visible = visible
        self.type = "Sun"
    def tick(self):
        pass
    def render(self):
        if self.visible:
            x,y = (self.x-game.width//2)*game.zoom + game.width//2, (self.y-game.height//2)*game.zoom + game.height//2
            pygame.draw.circle(game.win, (self.color), (int(x), int(y)), int(self.size*game.zoom))
class Planet(object):
    def __init__(self, x,y, xVel, yVel, gravity):
        self.startX, self.startY = x,y
        self.startXVel, self.startYVel = xVel, yVel
        self.fakeX, self.fakeY = x,y
        self.fakeCVel, self.fakeYVel = xVel, yVel
        self.gravity = gravity
        self.size = 5
        self.color = (0,0,255)
        self.reset()
        self.angle = 0
        self.turnSpeed = -random.random()-2
        self.type = "Planet"
        self.image = pygame.image.load(game.imagePath+"earth.png")
        self.prerenders = []
        self.predicts = 1000
    def reset(self):
        self.x, self.y = self.startX, self.startY
        self.xVel, self.yVel = self.startXVel, self.startYVel
        self.xAcc, self.yAcc = 0,0
    def tick(self):
        if game.move:
            self.angle += self.turnSpeed
            self.x += self.xVel
            self.y += self.yVel
            for g in game.objects:
                if g != self:
                    try:
                        self.xVel -= g.gravity * (self.x-g.x)/((self.x-g.x)**2+(self.y-g.y)**2)**1.5
                        self.yVel -= g.gravity * (self.y-g.y)/((self.x-g.x)**2+(self.y-g.y)**2)**1.5
                    except: pass
        if pygame.K_RETURN in game.keyPresses: self.reset()
    def render(self):
        x,y = (self.x-game.width//2)*game.zoom + game.width//2, (self.y-game.height//2)*game.zoom + game.height//2
        pygame.draw.circle(game.win, (self.color), (int(x), int(y)), int(self.size*game.zoom))
        if self.color == (0,0,255):
            image = self.image
            scale = 0.15*game.zoom
            image = pygame.transform.scale(image, (max(1,int(image.get_rect()[2]*scale)), max(1,int(image.get_rect()[3]*scale))))
            rotated = pygame.transform.rotate(image, self.angle)
            shift = rotated.get_rect()
            game.win.blit(rotated, (int(x-shift.center[0]), int(y-shift.center[1])))
        else:
            pygame.draw.circle(game.win, (self.color), (int(x), int(y)), max(1,int(self.size*game.zoom)))
    def fake(self):
        step = max(1,self.predicts//200)
        self.prerenders = [(self.x,self.y,self.xVel, self.yVel)]
        for g in game.objects:
            if g.type == "Planet" or g.type == "Player":
                g.fakeX, g.fakeY = g.x,g.y
                g.fakeXVel, g.fakeYVel = g.xVel, g.yVel
        for i in range(self.predicts):
            for g in game.objects:
                if g.type == "Planet" or g.type == "Player":
                    g.fakeTick()
        if True:
            try:
                for i in range(0,len(self.prerenders)-step,step):
                    pygame.draw.line(game.win, (0,0,255), (int((self.prerenders[i][0]-game.width//2)*game.zoom+game.width//2), int((self.prerenders[i][1]-game.height//2)*game.zoom+game.height//2)), (int((self.prerenders[i+step][0]-game.width//2)*game.zoom+game.width//2), int((self.prerenders[i+step][1]-game.height//2)*game.zoom+game.height//2)), 2)
            except:
               print("error")
    def fakeTick(self):
        for g in game.objects:
            if g != self:
                try:
                    if g.type == "Sun":
                        self.fakeXVel -= g.gravity * (self.fakeX-g.x)/((self.fakeX-g.x)**2+(self.fakeY-g.y)**2)**1.5
                        self.fakeYVel -= g.gravity * (self.fakeY-g.y)/((self.fakeX-g.x)**2+(self.fakeY-g.y)**2)**1.5
                    elif g.type == "Planet":
                        self.fakeXVel -= g.gravity * (self.fakeX-g.fakeX)/((self.fakeX-g.fakeX)**2+(self.fakeY-g.fakeY)**2)**1.5
                        self.fakeYVel -= g.gravity * (self.fakeY-g.fakeY)/((self.fakeX-g.fakeX)**2+(self.fakeY-g.fakeY)**2)**1.5
                except: pass
        self.fakeX += self.fakeXVel
        self.fakeY += self.fakeYVel
        self.prerenders.append((round(self.fakeX),round(self.fakeY)))

class Dart(Dart):
    def render(self):
        super().render()
        if self.throw.type == "Player" or self.throw.type == "Planet": self.throw.fake()
class Arrow(Arrow):
    def render(self):
        super().render()
        self.start.fake()
class Weight(Weight):
    def render(self):
        super().render()
        if self.obj.type == "Player" or self.obj.type == "Planet": self.obj.fake()


game = Game(1920,1016, getFPS(), 144)
Main(game)
