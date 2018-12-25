import numpy as np
import cv2

import math_util

# Dodger graphical constants
kDodgerImageFilename = 'resources/dodgermk2.png'
kDodgerRadius = 18 # image is 35x35
kDodgerColor = 0xFFFFFF
kDodgerColorScaleFactor = kDodgerColor/0x0000FF # because cv2 imread reads in scale 0-255

class Dodger:
   # Member variables:
   # float center_x_
   # float center_y_
   # float theta_
   # float speed_
   # float turning_rate_
   # cv.mat (numpy array) dodger_template_
   
   def __init__(self, cx, cy, theta, speed, turning_rate):
      self.center_x_ = cx
      self.center_y_ = cy
      self.theta_ = theta
      self.speed_ = speed
      self.turning_rate_ = turning_rate
      self.dodger_template_ = cv2.imread(kDodgerImageFilename, cv2.IMREAD_GRAYSCALE)
      
   # Draws dodger onto the input pixels matrix.
   # Returns 0 if dodger is still alive, or
   # nonzero if dodger has collided with something.
   def Draw(self, pixels):
      center = (math_util.RoundToInt(self.center_x_), math_util.RoundToInt(self.center_y_))
      working_pixels = math_util.SliceWorkingPixels(center, kDodgerRadius, pixels)
      # Compute rotation matrix
      center = (kDodgerRadius, kDodgerRadius)
      angle = -math_util.RadToDeg(self.theta_)
      # cv2.getRotationMatrix2D(center, angle, scale)
      rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)
      # Apply rotation matrix
      # cv2.warpAffine(src, M, dsize[, dst[, flags[, borderMode[, borderValue]]]])
      rotated_dodger = cv2.warpAffine(self.dodger_template_, rotation_matrix, working_pixels.shape)
      final_dodger = rotated_dodger.astype('uint32') * kDodgerColorScaleFactor
      dodger_mask = final_dodger > working_pixels
      collision_flag = np.any(working_pixels[dodger_mask])
      working_pixels[dodger_mask] = final_dodger[dodger_mask]
      return collision_flag
      
   # Updates dodger's center point based on speed and time
   def Move(self, dt):
      distance = self.speed_ * dt
      self.center_x_ += -distance * np.cos(self.theta_)
      self.center_y_ += distance * np.sin(self.theta_)
