# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

# Import section
from fortuneengine.GameEngineElement import GameEngineElement
from Constants import *
from AnswerMenu import AnswerMenuHolder
import pygame
import random

ADDNUM = 1
SUBNUM = 2
MULNUM = 3
DIVNUM = 4

class PPGame(GameEngineElement):

    def __init__(self):
        GameEngineElement.__init__(self, has_draw=True, has_event=True)
        sound = pygame.mixer.music.load(SOUND_PATH+ 'background_music.wav')
        #pygame.mixer.music.play(100, 0)
        self.score = [0,0]
        #[correct, incorrect]
        self.lastCorrect = 2
        #0 = wrong, 1 = right, 2 = skip drawing, 3 = enter a guess!
        self.images = {}
        self.__load_images()
        self.player_input = ''
        self.__setup()

        self.add_to_engine()
        
    def menu_callback(self, selection, menu):
        if selection == 'enter':
            if self.player_input == '':
                self.player_input = '0'
            self.__update()
        elif selection == 'clear':
                self.player_input = ''
        else:
                self.player_input = self.player_input + selection
        
    def __load_images(self):
        apple = pygame.image.load(IMAGE_PATH + "apple.png").convert_alpha()
        orange = pygame.image.load(IMAGE_PATH + "orange.png").convert_alpha()
        banana = pygame.image.load(IMAGE_PATH + "banana.png").convert_alpha()
        plum = pygame.image.load(IMAGE_PATH + "plum.png").convert_alpha()
        pear = pygame.image.load(IMAGE_PATH + "pear.png").convert_alpha()
        mango = pygame.image.load(IMAGE_PATH + "mango.png").convert_alpha()
        strawberry = pygame.image.load(IMAGE_PATH + "strawberry.png").convert_alpha()
        kiwi = pygame.image.load(IMAGE_PATH + "kiwi.png").convert_alpha()
        watermelon = pygame.image.load(IMAGE_PATH + "watermelon.png").convert_alpha()
        mult = pygame.image.load(ICON_PATH + "multiply.png").convert_alpha()
        div = pygame.image.load(ICON_PATH + "divide.png").convert_alpha()
        add = pygame.image.load(ICON_PATH + "plus.png").convert_alpha()
        sub = pygame.image.load(ICON_PATH + "minus.png").convert_alpha()
        equals = pygame.image.load(ICON_PATH + "equals.png").convert_alpha()
        
        self.images["apple"] = apple
        self.images["orange"] = orange
        self.images["banana"] = banana
        self.images["plum"] = plum
        self.images["pear"] = pear
        self.images["mango"] = mango
        self.images["strawberry"] = strawberry
        self.images["kiwi"] = kiwi
        self.images["watermelon"] = watermelon
        self.images[MULNUM] = mult
        self.images[DIVNUM] = div
        self.images[ADDNUM] = add
        self.images[SUBNUM] = sub
        self.images["equals"] = equals
                
    def remove_from_engine(self):
        super( PPGame, self ).remove_from_engine()
        
    def add_to_engine(self):
        super( PPGame, self).add_to_engine()
                    
    # Main game function
    def __setup(self):
        
        #fruit reference dict
        fruit_dictionary = {1:"apple", 2:"orange", 3:"banana", 4:"plum",
                           5:"pear", 6:"mango", 7:"strawberry", 8:"kiwi", 9:"watermelon"}
        
        self.fruit_list = []
        self.player_input = '' 
        
        # Declare row and column sum arrays.
        self.indexes = []
        self.Lsum = 0
        self.Rnum = 0
        self.answer = 0
        
        random.seed()
        #index[] 0 and 1 are the operations in the equation
        #index[2] is the fruit appearing again on the right side
        self.indexes.append(random.randint(1,4))
        self.indexes.append(random.randint(1,4))
        self.indexes.append(random.randint(0,1))
        self.fruit_list.append(self.images[fruit_dictionary[random.randint(1,4)]])
        self.fruit_list.append(self.images[fruit_dictionary[random.randint(5,9)]])

        #build the Left Side of the equation
        if self.indexes[0] == ADDNUM:
            self.Lsum = self.reverse_lookup(fruit_dictionary, self.reverse_lookup(self.images, self.fruit_list[0])) + self.reverse_lookup(fruit_dictionary, self.reverse_lookup(self.images, self.fruit_list[1]))
        elif self.indexes[0] == SUBNUM:
            self.Lsum = self.reverse_lookup(fruit_dictionary, self.reverse_lookup(self.images, self.fruit_list[0])) - self.reverse_lookup(fruit_dictionary, self.reverse_lookup(self.images, self.fruit_list[1]))
        elif self.indexes[0] == MULNUM:
            self.Lsum = self.reverse_lookup(fruit_dictionary, self.reverse_lookup(self.images, self.fruit_list[0])) * self.reverse_lookup(fruit_dictionary, self.reverse_lookup(self.images, self.fruit_list[1]))
            if self.Lsum == 0:
                self.__setup()
        elif self.indexes[0] == DIVNUM:
            self.Lsum = self.reverse_lookup(fruit_dictionary, self.reverse_lookup(self.images, self.fruit_list[0])) / self.reverse_lookup(fruit_dictionary, self.reverse_lookup(self.images, self.fruit_list[1]))
            if self.Lsum == 0:
                self.__setup()
        
        self.answer = self.reverse_lookup(fruit_dictionary, self.reverse_lookup(self.images, self.fruit_list[~(self.indexes[2]) & 1]))
        
        #Build the right unknown
        if self.indexes[1] == ADDNUM:
            self.Rnum = self.Lsum - self.reverse_lookup(fruit_dictionary, self.reverse_lookup(self.images, self.fruit_list[self.indexes[2]]))
        elif self.indexes[1] == SUBNUM:
            self.Rnum = self.Lsum + self.reverse_lookup(fruit_dictionary, self.reverse_lookup(self.images, self.fruit_list[self.indexes[2]]))
        elif self.indexes[1] == MULNUM:
            self.Rnum = self.Lsum / self.reverse_lookup(fruit_dictionary, self.reverse_lookup(self.images, self.fruit_list[self.indexes[2]]))
        elif self.indexes[1] == DIVNUM:
            self.Rnum = self.Lsum * self.reverse_lookup(fruit_dictionary, self.reverse_lookup(self.images, self.fruit_list[self.indexes[2]]))

    def reverse_lookup(self, d, v):
        for k in d:
            if d[k] == v:
                return k
        raise ValueError
        
    def __check(self):
        if(self.player_input == ''):
            self.lastCorrect = 3
        elif(int(self.player_input) == self.answer):
            self.score[0] += 1
            self.lastCorrect = 1
            self.__setup()
        else:
            self.score[1] += 1
            self.lastCorrect = 0
            self.lastAnswer = self.answer
            self.__setup()
        
        
    def __update(self):
        self.game_engine.get_object('answermenu').remove_from_engine()
        
    def event_handler(self, event):
        """Update the menu and get input for the menu."""
        return_val = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return_val = True
                self.__check()
                self.game_engine.set_dirty()
            if event.key == (pygame.K_LSHIFT or pygame.K_RSHIFT):
                return_val = True
                self.game_engine.set_dirty()
                self.game_engine.add_object('answermenu', AnswerMenuHolder(self.menu_callback))
                self.game_engine.get_object('answermenu').show_menu('enter')
    
    def draw(self,screen,time_delta):
        fruit_dictionary = {1:"apple", 2:"orange", 3:"banana", 4:"plum",
                5:"pear", 6:"mango", 7:"strawberry", 8:"kiwi", 9:"watermelon"}
        
        #draw background & setup
        bg = pygame.image.load(IMAGE_PATH + "bg.gif").convert()
        screen.blit(bg,(0,0))
        font = pygame.font.Font(None, 24)
        ren = font.render("Press shift to enter guess. Press enter to check solution!", 1, [255,255,255])
        screen.blit(ren, (20, 630))
        font = pygame.font.Font(None, 64)
        ren = font.render("Solve the Equation!", 1, [0,0,0])
        screen.blit(ren, (275, 120))
        
        
        #First Equation
        x = 250
        y = 220
        for fruit in self.fruit_list:
            screen.blit(fruit, (x,y))
            x += 140
        screen.blit(self.images[self.indexes[0]], (320, y+5))
        screen.blit(self.images["equals"], (x - 45, y+5))
        ren = font.render(str(self.Rnum), 1, [0, 0, 0])
        screen.blit(ren, (x+35,y+5))
        screen.blit(self.images[self.indexes[1]], (x+105, y+5))
        screen.blit(self.fruit_list[self.indexes[2]], (x+175, y))
        
        #second equation
        x=390
        y=320
        screen.blit(self.fruit_list[self.indexes[2]], (x,y))
        screen.blit(self.images["equals"], (x+70,y+5))
        ren = font.render(str(self.reverse_lookup(fruit_dictionary, self.reverse_lookup(self.images, self.fruit_list[self.indexes[2]]))), 1, [0,0,0])
        screen.blit(ren, (x+140,y))
        
        #third equation
        x=390
        y=420
        #nand to get opposite fruit
        screen.blit(self.fruit_list[~(self.indexes[2]) & 1], (x,y))
        screen.blit(self.images["equals"], (x+70,y+5))
        if self.player_input == '':
            ren = font.render("?",1,[0,0,0])
            screen.blit(ren,(x+140,y))
        else:
            ren = font.render(self.player_input,1,[0,0,0])
            screen.blit(ren,(x+140,y))
            
        #draw score and last guess in/correct
        font = pygame.font.Font(None, 24)
        if(self.lastCorrect == 0): 
            ren = font.render("Almost! The answer was " + str(self.lastAnswer), 1, [255,255,255])
        elif(self.lastCorrect == 1):
            ren = font.render("Good job!", 1, [255,255,255])
        elif(self.lastCorrect == 3):
            ren = font.render("Oops, you forgot to enter an answer.", 1, [255,255,255])
        
        if(self.lastCorrect != 2):
            screen.blit(ren, (20, 602))
            
        ren = font.render("#Correct = " + str(self.score[0]) + " and #Incorrect = " + str(self.score[1]), 1, [255,255,255])
        screen.blit(ren, (670,630))
            
        

