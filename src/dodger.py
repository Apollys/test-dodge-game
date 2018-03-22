import numpy as np
import cv2

class Dodger:
   # member variables:
   # all floats: center_x, center_y, theta, speed
   
   UNIT_TEMPLATE = im = cv2.imread('dodgermk1.png', cv2.IMREAD_GRAYSCALE)
   RADIUS = 18 # image is 35x35
   DEGREES_PER_RADIAN = 180.0/np.pi
   
   def __init__(self, cx, cy, theta, speed):
      self.center_x = cx
      self.center_y = cy
      self.theta = theta
      self.speed = speed
      
   def draw(self, pixels):
      cx = int(self.center_x + 0.5)
      cy = int(self.center_y + 0.5)
      r = self.RADIUS
      working_pixels = pixels[cy-r:cy+r+1, cx-r:cx+r+1]
      # Rotation matrix
      rotation_matrix = cv2.getRotationMatrix2D((r, r), self.theta*Dodger.DEGREES_PER_RADIAN, 1)
      rotated_unit = cv2.warpAffine(Dodger.UNIT_TEMPLATE, rotation_matrix, working_pixels.shape)
      mask = rotated_unit > working_pixels
      working_pixels[mask] = rotated_unit[mask]
      