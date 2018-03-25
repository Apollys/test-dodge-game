import sys
import numpy as np
import keyboard
import pygame
from timeit import default_timer as timer

import circle
import dodger
import time

class Canvas:

   FRAMERATE = 60
   BORDER_COLOR = 0xA0A0A0

   # member variables:
   # title - window title
   # resolution - 2-tuple
   # screen - pygame screen obj
   # pixels - pygame surfarray
   # clock - pygame clock to track times and framerates
   # background - numpy array containing data that stays constant between frames
   # borders - (2, 2) numpy array [ [xmin, xmax], [ymin, ymax] ]
   # border_width
   # pixels - numpy array containing active pixel data
   # previous_pixels - previous frame (for input into machine learning)
   # circles - list of Circle objects
   # dodger_obj
   # collision_flag
   # score
   
   def __init__(self, xres, yres, title=''):
      # basic window properties
      self.title = title
      pygame.display.set_caption(title) # Correct usage?
      self.resolution = (xres, yres)
      self.screen = pygame.display.set_mode(self.resolution)
      
      # pixel array
      self.pixels = pygame.surfarray.pixels2d(self.screen) # Modifying these pixels will update the screen @ pygame.flip()
      self.previous_pixels = np.zeros(self.resolution, dtype='uint32')
      
      # clock
      self.clock = pygame.time.Clock()
      
      # background array, will hold the static elements like borders
      self.background = np.zeros(self.resolution, dtype='uint32')
      np.copyto(self.pixels, self.background)
      
      # compute helpful border values for later
      self.border_width = 10
      edge = 2*self.border_width
      self.borders = np.array([[edge-1, xres-edge], [edge-1, yres-edge]], dtype='float16')
      
      # dynamic objects
      self.circles = []
      self.dodger_obj = None # To be initialized later
      self.collision_flag = False
      
      # FPS caluclation objects
      self.start_timer = timer()
      self.frame_count = 0
      
      self.score = 0
      
      # expects a function that takes event as parameter
      # keyboard.on_press_key('esc', lambda event: self.close_game())
      
      # done initializing canvas
      print('Canvas initialized', self.borders)
      
   
   #########################################
   ### Some basic initialization methods ###
   #########################################
   
   def draw_borders(self):
      bw = self.border_width
      self.background[bw:-bw, bw:2*bw] = Canvas.BORDER_COLOR
      self.background[bw:-bw, -2*bw:-bw] = Canvas.BORDER_COLOR
      self.background[bw:2*bw, bw:-bw] = Canvas.BORDER_COLOR
      self.background[-2*bw:-bw, bw:-bw] = Canvas.BORDER_COLOR

   def create_dodger(self, cx, cy, theta, speed):
      self.dodger_obj = dodger.Dodger(cx, cy, theta, speed)
      
   def add_circle(self, cx, cy, radius, vx, vy):
      self.circles.append(circle.Circle(cx, cy, radius, vx, vy))
      
      
   #########################################
   ###       Movement computations       ###
   #########################################

   # modifies "abstract" variables but not pixels
   def time_step(self):
      dt = self.clock.tick(Canvas.FRAMERATE)
      # todo: include the amount of time (delta_t) between frames in movement computations
      self.move_circles()
      if (self.dodger_obj):
         self.dodger_obj.move()
  
   def move_circles(self):
      # Note: centers and velocities are floats for accuracy, the circle drawing method deals with rounding
      for cir in self.circles:
         cir.center += cir.velocity
         minx, miny = cir.center - cir.radius
         maxx, maxy = cir.center + cir.radius
         (bminy, bmaxy), (bminx, bmaxx) = self.borders
         overx = max(0.0, maxx - bmaxx)
         overy = max(0.0, maxy - bmaxy)
         underx = max(0.0, bminx - minx)
         undery = max(0.0, bminy - miny)
         # left/right bounce
         if (overx or underx):
            cir.velocity[0] *= -1.0
         # top/bottom bounce
         if (overy or undery):
            cir.velocity[1] *= -1.0
         # correction
         cir.center[0] += 2.0*(underx - overx)
         cir.center[1] += 2.0*(undery - overy)
               
               
   #########################################
   ###       Pixel update methods        ###
   #########################################
   
   # update self.pixels to include foreground objects
   def draw_foreground(self):
      for c in self.circles:
         c.draw(self.pixels)
      if (self.dodger_obj):
         # dodger.draw() returns collision flag
         self.collision_flag = self.dodger_obj.draw(self.pixels)
         
      
   # create next frame in self.pixels
   def draw_next_frame(self):
      np.copyto(self.previous_pixels, self.pixels)
      np.copyto(self.pixels, self.background)
      self.time_step()
      self.draw_foreground()

         
   #########################################
   ###        User Input Management      ###
   #########################################         
   
   # exit
   def close_game(self):
      pygame.display.quit()
      pygame.quit()
      end_timer = timer()
      fps = self.frame_count/(end_timer - self.start_timer)
      print('Game loop completed, fps =', fps)
      sys.exit()
   
   # called each frame to process user input
   def check_keyboard(self):
      # A/D to modify ship's facing
      if (self.dodger_obj):
         dtheta = self.dodger_obj.turning_rate
         if (keyboard.is_pressed('a')):
            self.dodger_obj.theta += dtheta
         if (keyboard.is_pressed('d')):
            self.dodger_obj.theta -= dtheta
      # escape to quite at any time
      if (keyboard.is_pressed('esc')):
         self.close_game()
   
   # wait for spacebar, and display corresponding message to console
   def pause(self):
      print('Press [space] to continue...')
      pressed_key = ''
      while ((pressed_key != 'space') and (pressed_key != 'esc')):
         pressed_key = keyboard.read_key()
      if (pressed_key == 'esc'):
         self.close_game()
      
   
   ### For machine learning, compute encoded pixels of last 2 frames ###
   def compute_ai_input(self):
      pass
      
   
   
   ### Render next frame ###
   # Process input, update game state, update pixels matrix, render (pygame.flip())
   def render_next_frame(self):
      self.check_keyboard()
      self.draw_next_frame()
      pygame.display.flip()   
      if (self.collision_flag):
         print('You have crashed!  Total score:', self.score)
         self.close_game()
         self.pause()

      
   #########################################
   ###     External API Starts Here      ###
   ######################################### 
   
   ### Top-level loop ###
   def main_game_loop(self, max_frames=-1):
      self.start_timer = timer()
      self.frame_count = 0
      while (self.frame_count != max_frames):
         self.render_next_frame()
         self.frame_count += 1
         self.score += 1
      self.close_game()
         
   
   ### Single Frame Display ###
   def render_single_frame(self, pause=True):
      self.check_keyboard()
      self.draw_next_frame()
      pygame.display.flip()  
      if (pause):
         self.pause()
   
      
      