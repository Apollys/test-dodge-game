import numpy as np
import cv2

class Circle:
   # member variables:
   # center - numpy array of shape (2,)
   # radius
   # velocity - numpy array of shape (2,)
   
   CIRCLE_COLOR = 200
   
   def __init__(self, cx, cy, r, vx=0, vy=0):
      self.center = np.array([cx, cy], dtype='float16')
      self.radius = r
      self.velocity = np.array([vx, vy], dtype='float16')
      
   def draw(self, pixels):
      # snap float values to integer values
      cx, cy = (self.center+0.5).astype(int)
      r = self.radius
      # grab the subsection of the screen = square in which the circle is inscribed
      working_pixels = pixels[cy-r:cy+r+1, cx-r:cx+r+1]
      mask = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2*r+1, 2*r+1)).astype(bool)
      working_pixels[mask] = Circle.CIRCLE_COLOR
      
      