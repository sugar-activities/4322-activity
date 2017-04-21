# -*- coding: utf-8 -*-
#
#       PPGameManager.py
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
import pygame
from fortuneengine.GameEngineElement import GameEngineElement
from PPGame import PPGame


class PPGameManager(GameEngineElement):
    def __init__(self):
        GameEngineElement.__init__(self, has_draw=False, has_event=True)
        self.add_to_engine()

        game_size_ratio_x = self.game_engine.width/1200.0
        game_size_ratio_y = self.game_engine.height/900.0

        term_width_offset = game_size_ratio_x * 200
        term_height = game_size_ratio_y * 200
        term_height_offset = game_size_ratio_y * 700
        term_width = game_size_ratio_x * 1000



        #self.game_engine.add_object('game', PPGameHolder())

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            newKey=pygame.key.name(event.key)
            if newKey=='escape':
                self.game_engine.stop_event_loop()
                return True


