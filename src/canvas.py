import cv2
import numpy as np

import circle
import dodger

class Canvas:
   # member variables:
   # title - window title
   # resolution - 2-tuple
   # background - numpy array containing data that stays constant between frames
   # borders - (2, 2) numpy array [ [xmin, xmax], [ymin, ymax] ]
   # border_width
   # pixels - numpy array containing active pixel data
   # circles - list of Circle objects
   # dodger_obj
   
   def __init__(self, xres, yres, title=''):
      self.title = title
      self.resolution = (xres, yres)
      self.background = np.zeros(self.resolution, dtype='uint8')
      self.border_width = 10
      edge = 2*self.border_width
      self.borders = np.array([[edge-1, xres-edge], [edge-1, yres-edge]], dtype='float16')
      self.pixels = np.copy(self.background)
      self.circles = []
      self.dodger_obj = None # To be initialized later
      print('Canvas initialized, borders =', self.borders)

   def create_dodger(self, cx, cy, theta, speed):
      self.dodger_obj = dodger.Dodger(cx, cy, theta, speed)
      
   def draw_borders(self):
      border_value = 150
      bw = self.border_width
      self.background[bw:-bw, bw:2*bw] = border_value
      self.background[bw:-bw, -2*bw:-bw] = border_value
      self.background[bw:2*bw, bw:-bw] = border_value
      self.background[-2*bw:-bw, bw:-bw] = border_value
      
   def add_circle(self, cx, cy, radius, vx, vy):
      self.circles.append(circle.Circle(cx, cy, radius, vx, vy))
      
   def draw_foreground(self):
      # Draw all foreground objects, which for now is just circles
      for c in self.circles:
         c.draw(self.pixels)
      if (self.dodger_obj):
         self.dodger_obj.draw(self.pixels)
      
   def start_new_frame(self):
      self.pixels = np.copy(self.background)

   def key_callback(self, key_pressed):
      # A/D to modify ship's facing
      dtheta = 0.1
      if (key_pressed == ord('a')):
         self.dodger_obj.theta += dtheta
      elif (key_pressed == ord('d')):
         self.dodger_obj.theta -= dtheta
      
      
   def render(self, wait=0):
      cv2.imshow(self.title, self.pixels)
      if (wait <= 0):
         print('Press any key to continue...')
      key_pressed = cv2.waitKey(wait)
      if (key_pressed > -1):
         self.key_callback(key_pressed & 0xFF)
      
   def render_new_frame(self, wait=0):
      self.start_new_frame()
      self.draw_foreground()
      self.render(wait)

   def move_circles(self):
      # oversimplified method, balls will go inside walls
      # correct way would be to move them, then check if they went into wall, then correct it
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
      
   def time_step(self):
      self.move_circles()