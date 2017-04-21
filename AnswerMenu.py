import pygame
from fortuneengine.GameEngineElement import GameEngineElement
from Constants import IMAGE_PATH
from gettext import gettext as _

NORMAL_MENU = 1
GRID_MENU = 3

class AnswerMenuHolder( GameEngineElement ):
    def __init__(self, callback):
        GameEngineElement.__init__(self, has_draw=False, has_event=False)
        self.menu = None
        self.callback = callback
        self.font = pygame.font.SysFont("cmr10",26,False,False)
        self.add_to_engine()

    def remove_from_engine(self):
        super( AnswerMenuHolder, self ).remove_from_engine()
        self.clear_menu()

    def menu_called(self, id):
        self.callback(id, self)

    def clear_menu(self):
        if self.menu:
            self.menu.remove_from_engine()
            self.menu = None

    def show_menu(self,id):
        if self.is_in_engine():
            self.clear_menu()
        else:
            self.add_to_engine()
            
        if id == "enter":
            menu_type = GRID_MENU
            menu_options = [
                        ['1', lambda: self.menu_called('1')],
                        ['2', lambda: self.menu_called('2')],
                        ['3', lambda: self.menu_called('3')],
                        ['4', lambda: self.menu_called('4')],
                        ['5', lambda: self.menu_called('5')],
                        ['6', lambda: self.menu_called('6')],
                        ['7', lambda: self.menu_called('7')],
                        ['8', lambda: self.menu_called('8')],
                        ['9', lambda: self.menu_called('9')],
                        [_("C"), lambda: self.menu_called('clear')],
                        ['0', lambda: self.menu_called('0')],
                        [_("E"), lambda: self.menu_called('enter')],
            ]
        else:
            print "Invalid Menu", id
            return
        self.menu = AnswerMenu(menu_options)
        
class AnswerMenu(GameEngineElement):
    def __init__(self, options):
        GameEngineElement.__init__(self, has_draw=True, has_event=True)

        self.menu = Menu(options)

        self.menu.set_pos(650, 420)
        self.add_to_engine()

    def event_handler(self, event):
        self.game_engine.set_dirty()
        return self.menu.update(event)

    def draw(self,screen,time_delta):
        self.menu.draw( screen )

class Menu(object):
    def __init__(self, options):
        """Initialize the EzMenu! options should be a sequence of lists in the
        format of [option_name, option_function]"""

        self.options = options
        self.x = 0
        self.y = 0
        self.cols = 3
        self.font = pygame.font.SysFont("cmr10",24,False,False)
        self.option = 0
        self.width = 1
        self.color = [0, 0, 0]
        self.hcolor = [255, 0, 0]
        self.height = len(self.options)*self.font.get_height()

    def draw(self, surface):
        """Draw the menu to the surface."""
        i=0 # Row Spacing
        h=0 # Selection Spacing
        j=0 # Col Spacing
        xoff = 198/3 - 1
        yoff = 248/4 - 1
        for o in self.options:
            if h==self.option:
                clr = self.hcolor
            else:
                clr = self.color
                
            text = o[0]
            ren = self.font.render(text, 1, clr)
            if ren.get_width() > self.width:
                self.width = ren.get_width()

            newX = self.x + xoff * j
            newY = self.y+ i * yoff            
            pygame.draw.rect(surface, (0, 0, 255), ( newX, newY, 62, 58))
            pygame.draw.rect(surface, (4, 119, 152), ( newX + 2, newY + 2, 58, 54))
            surface.blit(ren, (newX + 26, newY + 26))

            j+=1
            h+=1
            if j >= self.cols:
                i+=1
                j=0

    def update(self, event):
        """Update the menu and get input for the menu."""
        return_val = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if self.cols != 1:
                    self.option += self.cols
                else:
                    self.option += 1
                return_val = True
            elif event.key == pygame.K_UP:
                if self.cols != 1:
                    self.option -= self.cols
                else:
                    self.option -= 1
                return_val = True
            elif event.key == pygame.K_RIGHT:
                if self.cols != 1:
                    self.option += 1
                    return_val = True
            elif event.key == pygame.K_LEFT:
                if self.cols != 1:
                    self.option -= 1
                    return_val = True
            elif event.key == pygame.K_RETURN:
                self.options[self.option][1]()
                return_val = True

            self.option = self.option % len(self.options)
        return return_val

    def set_pos(self, x, y):
        """Set the topleft of the menu at x,y"""
        self.x = x + 3
        self.y = y + 51
