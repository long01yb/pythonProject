# from Window import Window
# from button import Button
#
#
# class SelectCharacter(Window):
#     def initButtons(self):
#         self.buttons.add("character1",Button())
#         self.buttons.add("character1", Button())
#     def __init__(self,background,screen,windowStack):
#         super().__init__(background,screen,windowStack)

if self.state == self.COLLISION:
    self.locked.acquire()
    while self.ques.isTHINKING():
        self.ques.update()
        self.ques.getAnswer()
        self.ques.draw()
        print("1")
    self.locked.release()
    if self.ques.isTrue():
        self.player.heal()
    self.ques.refresh()
    self.ques.updateContent()
    self.inc = self.talk_to_player.continue_game()
    self.state = self.PLAYING
    pygame.display.update()
