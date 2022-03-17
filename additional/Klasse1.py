class main(object):
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.objects = []
    def set_window(self):
        self.win = pygame.display.set_mode((self.width, self.height))
    def tick(self):
        for object in self.objects:
            object.tick()
    def render(self):
        for object in self.objects:
            object.render()



