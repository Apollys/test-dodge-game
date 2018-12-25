import numpy as np
import cv2

import math_util

# Circle constants
kCircleColor = 0xAA55D0

class Circle:
   # member variables:
   # numpy.array center_  # shape: (2, ), dtype: float16
   # float/int? radius_
   # numpy.array velocity_  # shape (2, ), dtype: float16
   
   def __init__(self, cx, cy, r, vx=0, vy=0):
      self.center_ = np.array([cx, cy], dtype='float16')
      self.radius_ = r
      self.velocity_ = np.array([vx, vy], dtype='float16')
      
   # Draws circle onto the pixels matrix.
   # No return value.
   def Draw(self, pixels):
      working_pixels = math_util.SliceWorkingPixels(self.center_, self.radius_, pixels)
      circle_mask_size = (2 * self.radius_ + 1, 2 * self.radius_ + 1)
      # cv2.getStructuringElement(shape, ksize[, anchor]), where shape is some cv2 constant
      circle_mask = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, circle_mask_size).astype(bool)
      working_pixels[circle_mask] = kCircleColor
