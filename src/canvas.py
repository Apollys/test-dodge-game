import sys
import numpy as np
import keyboard  # Todo: freeze a version of this and make it part of this project's source
import pygame
from timeit import default_timer as timer

import circle
import dodger
import time
import math_util

# Canvas constants
kFramerate = 60
kBorderColor = 0xA0A0A0
kBorderWidth = 20

class Canvas:
   # Member variables:
   # string window_title_
   # 2-tuple <int> resolution_
   # int border_width_
   # pygame.screen(?) screen_
   # pygame.surfarray(?) pixels_  # this should just be a numpy array, verify
   # numpy.array previous_pixels_  # dtype:uint32, previous frame (for machine learning)
   # pygame.clock(?) clock_
   # numpy.array background_  # dtype: uint32, contains data that stays constant between frames
   # 2-tuple <int> playable_area_xrange_
   # 2-tuple <int> playable_area_yrange_
   # list circles_  # element type: Circle
   # Dodger dodger_object_
   # boolean collision_flag_v
   # timer start_time_
   # int frame_count_
   # int score_
   
   def __init__(self, xres, yres, window_title=''):
      # Basic window properties
      self.window_title_ = window_title
      pygame.display.set_caption(self.window_title_) # Correct usage?
      self.resolution_ = (xres, yres)
      self.border_width_ = kBorderWidth
      self.screen_ = pygame.display.set_mode(self.resolution_)
      # Pixel arrays
      # Modifying pixels_ will update the screen @ pygame.flip()
      self.pixels_ = pygame.surfarray.pixels2d(self.screen_)
      self.previous_pixels_ = np.zeros(self.resolution_, dtype='uint32')
      # Clock
      self.clock_ = pygame.time.Clock()
      # Background array, will hold the static elements like borders
      self.background_ = np.zeros(self.resolution_, dtype='uint32')
      np.copyto(self.pixels_, self.background_)
      # Compute main playing field borders
      xmin = kBorderWidth
      xmax = (xres - 1) - kBorderWidth
      ymin = kBorderWidth
      ymax = (yres - 1) - kBorderWidth
      self.playable_area_xrange_ = (xmin, xmax)
      self.playable_area_yrange_ = (ymin, ymax)
      # Dynamic objects
      self.circles_ = []
      self.dodger_object_ = None  # to be initialized later
      self.collision_flag_ = False
      # FPS caluclation objects
      self.start_time_ = timer()
      self.frame_count_ = 0
      # Score
      self.score_ = 0
      # Is this ever needed? Delete?
      # expects a function that takes event as parameter
      # keyboard.on_press_key('esc', lambda event: self.close_game())
      
      # Done initializing canvas
      print('Canvas initialized')
      
   
   #########################################
   ### Some basic initialization methods ###
   #########################################
   
   # Draws borders onto the background_ matrix
   def DrawBorders(self):
      # Leave a black border of half the border width around outside,
      # then draw border of other half of border width inside that padding
      xmin, xmax = self.playable_area_xrange_
      ymin, ymax = self.playable_area_yrange_
      padding = math_util.RoundToInt(0.5 * kBorderWidth)
      self.background_[padding:xmin-1, padding:-padding] = kBorderColor
      self.background_[xmax+1:-padding, padding:-padding] = kBorderColor
      self.background_[padding:-padding, padding:ymin-1] = kBorderColor
      self.background_[padding:-padding, ymax+1:-padding] = kBorderColor

   def CreateDodger(self, cx, cy, theta, speed, turning_rate):
      self.dodger_object_ = dodger.Dodger(cx, cy, theta, speed, turning_rate)
      
   def AddCircle(self, cx, cy, radius, vx, vy):
      self.circles_.append(circle.Circle(cx, cy, radius, vx, vy))
      
      
   #########################################
   ###       Movement computations       ###
   #########################################

   # Modifies "abstract" variables but not pixels
   def TimeStep(self):
      # this is causing excess stuttering, don't use return value of clock_.tick()
      dt_ms = self.clock_.tick(kFramerate)
      #dt = 0.001 * dt_ms
      dt = 1.0 / kFramerate
      self.MoveCircles(dt)
      if (self.dodger_object_):
         self.dodger_object_.Move(dt)
  
   def MoveCircles(self, dt):
      # Note: centers and velocities are floats for accuracy, the circle drawing method deals with rounding
      for circle_object in self.circles_:
         circle_object.center_ += circle_object.velocity_
         c_xmin, c_ymin = circle_object.center_ - circle_object.radius_
         c_xmax, c_ymax = circle_object.center_ + circle_object.radius_
         xmin, xmax = self.playable_area_xrange_
         ymin, ymax = self.playable_area_yrange_
         overx = max(0.0, c_xmax - xmax)
         overy = max(0.0, c_ymax - ymax)
         underx = max(0.0, xmin - c_xmin)
         undery = max(0.0, ymin - c_ymin)
         # Left/right bounce
         if (overx or underx):
            circle_object.velocity_[0] *= -1.0
         # Top/bottom bounce
         if (overy or undery):
            circle_object.velocity_[1] *= -1.0
         # Correction
         circle_object.center_[0] += 2.0 * (underx - overx)
         circle_object.center_[1] += 2.0 * (undery - overy)
               
               
   #########################################
   ###       Pixel update methods        ###
   #########################################
   
   # Update self.pixels_ to include foreground objects
   def DrawForeground(self):
      for circle_object in self.circles_:
         circle_object.Draw(self.pixels_)
      if (self.dodger_object_):
         self.collision_flag_ = self.dodger_object_.Draw(self.pixels_)

   # Draw next frame in self.pixels_
   def DrawNextFrame(self):
      np.copyto(self.previous_pixels_, self.pixels_)
      np.copyto(self.pixels_, self.background_)
      self.TimeStep()
      self.DrawForeground()

         
   #########################################
   ###        User Input Management      ###
   #########################################         
   
   # Exit
   def CloseGame(self):
      pygame.display.quit()
      pygame.quit()
      end_time = timer()
      fps = self.frame_count_ / (end_time - self.start_time_)
      print('Game loop completed, fps =', fps)
      sys.exit()
   
   # Called each frame to process user input
   def ProcessKeyboardInput(self):
      # A/D to modify ship's facing
      if (self.dodger_object_):
         dtheta = self.dodger_object_.turning_rate_
         if (keyboard.is_pressed('a')):
            self.dodger_object_.theta_ += dtheta
         if (keyboard.is_pressed('d')):
            self.dodger_object_.theta_ -= dtheta
      # Escape to quite at any time
      if (keyboard.is_pressed('esc')):
         self.CloseGame()
   
   # Wait for spacebar, and display corresponding message to console
   def Pause(self):
      print('Press [space] to continue...')
      pressed_key = ''
      while ((pressed_key != 'space') and (pressed_key != 'esc')):
         pressed_key = keyboard.read_key()
      if (pressed_key == 'esc'):
         self.CloseGame()
      
      
   #########################################
   ###            Render Frame           ###
   #########################################
      
   # Process input, update game state, update pixels matrix, render (pygame.flip())
   def RenderNextFrame(self):
      self.ProcessKeyboardInput()
      self.DrawNextFrame()
      pygame.display.flip()  # render
      if (self.collision_flag_):
         print('You have crashed!  Total score:', self.score_)
         self.CloseGame()
         self.Pause()
      
   
   ### For machine learning, compute encoded pixels of last 2 frames ###
   def compute_ai_input(self):
      pass

      
   #########################################
   ###     External API Starts Here      ###
   ######################################### 
   
   ### Top-level loop ###
   def MainGameLoop(self, max_frames=-1):
      self.start_time_ = timer()
      self.frame_count_ = 0
      while (self.frame_count_ != max_frames):
         self.RenderNextFrame()
         self.frame_count_ += 1
         self.score_ += 1
      self.CloseGame()
         
   
   ### Single Frame Display ###
   def RenderSingleFrame(self, pause=True):
      self.ProcessKeyboardInput()
      self.DrawNextFrame()
      pygame.display.flip() 
      if (self.collision_flag_):
         print('You have crashed!  Total score:', self.score_)
         self.CloseGame()
         self.Pause()
      if (pause):
         self.Pause()
   
      
      