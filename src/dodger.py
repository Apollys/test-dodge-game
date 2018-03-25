import numpy as np
import cv2

class Dodger:
   # member variables:
   # all floats: center_x, center_y, theta, speed
   
   UNIT_TEMPLATE = im = cv2.imread('dodgermk1.png', cv2.IMREAD_GRAYSCALE).T
   RADIUS = 18 # image is 35x35
   DEGREES_PER_RADIAN = 180.0/np.pi
   DODGER_COLOR = 0xFFFFFF
   DODGER_SCALE_FACTOR = DODGER_COLOR/0x0000FF # because cv2 imread reads in scale 0-255
   
   def __init__(self, cx, cy, theta, speed):
      self.center_x = cx
      self.center_y = cy
      self.theta = theta
      self.speed = speed
      self.turning_rate = .07
      
   # returns 0 if dodger has not collided with anything, else nonzero
   def draw(self, pixels):
      cx = int(self.center_x + 0.5)
      cy = int(self.center_y + 0.5)
      r = self.RADIUS
      working_pixels = pixels[cy-r:cy+r+1, cx-r:cx+r+1]
      # Rotation matrix
      rotation_matrix = cv2.getRotationMatrix2D((r, r), -self.theta*Dodger.DEGREES_PER_RADIAN, 1)
      rotated_unit = cv2.warpAffine(Dodger.UNIT_TEMPLATE, rotation_matrix, working_pixels.shape).astype('uint32')*Dodger.DODGER_SCALE_FACTOR
      mask = rotated_unit > working_pixels
      collision_flag = np.any(working_pixels[mask])
      working_pixels[mask] = rotated_unit[mask]
      return collision_flag
      
   def move(self, dt=1.0/60):
      d = self.speed*dt
      self.center_x += -d*np.cos(self.theta)
      self.center_y += -d*np.sin(self.theta)