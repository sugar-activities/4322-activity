# -*- coding: utf-8 -*-
#
#       PPMainMenu.py
#       
#       Copyright 2010 Kevin Hockey <blitz@blitzkev>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import pygame, ezmenu
from fortuneengine.GameEngineElement import GameEngineElement

class MainMenuHolder( GameEngineElement ):
    def __init__(self, callback, background=None, width=952, height=732):
        GameEngineElement.__init__(self, has_draw=True, has_event=False)
        self.menu = None
        self.callback = callback
        bg = pygame.image.load(background).convert()
        self.background = pygame.transform.scale(bg, (width, height))
        self.width = width
        self.height = height

    def remove_from_engine(self):
        super( MainMenuHolder, self ).remove_from_engine()
        self.clear_menu()

    def draw(self,screen,time_delta):
        if self.background:
            screen.blit(self.background,(0,0))
        else:
            screen.fill((0, 0, 255))

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

        if id == "title":
            menu_options = [
                        ["Produce Puzzle", lambda: self.show_menu("adventure"), "Begin a new game!"],
                        ["Exit Game", lambda: self.game_engine.stop_event_loop(), "Exit the game."]
            ]

        elif id == "adventure":
            menu_options = [
                        ["New Game",  lambda: self.menu_called("new"), "Start a new game."],
                        ["Return to Title", lambda: self.show_menu("title"), "Return to the title menu."]
            ]
        else:
            print "Invalid Menu", id
            return
        self.menu = MainMenu(menu_options, self.width, self.height)

class MainMenu(GameEngineElement):
    def __init__(self, game_menu, width=800, height=400):
        GameEngineElement.__init__(self, has_draw=True, has_event=True)
        self.menu = ezmenu.EzMenu(game_menu)
        self.menu.center_at(width - (width/3), height/2)
        self.menu.help_text_at( 0, height-(height/8))
        self.menu.set_font(pygame.font.SysFont("Arial", 20))
        self.menu.set_highlight_color((0, 255, 0))
        self.menu.set_normal_color((255, 255, 255))
        self.add_to_engine()

    def event_handler(self, event):
        self.game_engine.set_dirty()
        return self.menu.update(event)

    def draw(self,screen,time_delta):
        self.menu.draw( screen )
