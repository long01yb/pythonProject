import button


class Tab:
    THINKING = 1
    ISANSWER = 10
    def __init__(self,screen,background):
        self.screen = screen
        self.background = background
        self.buttonlist = button.ButtonList()
        self.state = self.THINKING
    def initButtons(self):
        pass
    def update(self):
        pass
    def draw(self):
        pass
    def run(self):
        pass