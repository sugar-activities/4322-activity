# -*- coding: utf-8 -*-
#
#       PPActivity.py
#       
#       Copyright 2010 Kevin Hockey <blitzkev@gmail.com>
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

from fortuneengine.GameEngine import GameEngine
from PPGameManager import PPGameManager
from PPMainMenu import MainMenuHolder
from PPGame import PPGame
from Constants import IMAGE_PATH

ge = GameEngine(width=952, height=714, always_draw=False)


def start_game():
    ge.add_object('manager', PPGameManager() )

def menu_screen():
    ge.add_object('menu', MainMenuHolder( menu_called, IMAGE_PATH + "bg.gif", width=ge.width, height=ge.height))
    ge.get_object('menu').show_menu('title')

def menu_called(id, menu):
    if id == 'new':
        menu.remove_from_engine()
        start_game()
        ge.remove_object('menu')
        ge.add_object('game', PPGame() )
    else:
        print "MENU CALLED %s" % id

# Build menu and add to engine.  Then show menu
menu_screen()

# Start event loop
ge.start_main_loop()
