import numpy as np
import random
   
def RoundToInt(float_value):
   return int(float_value + 0.5)

def RadToDeg(radians):
   return radians * 180.0 / np.pi
   
def DegToRad(degrees):
   return degrees * np.pi / 180.0

def SliceWorkingPixels(center, apothem, pixels):
   cx, cy = center
   cx_i = RoundToInt(cx)
   cy_i = RoundToInt(cy)
   min_x_i = cx_i - apothem
   max_x_i = cx_i + apothem + 1
   min_y_i = cy_i - apothem
   max_y_i = cy_i + apothem + 1
   #print('SliceWorkingPixels:')
   #print('center:', cx_i, cy_i)
   #print('x range:', min_x_i, max_x_i)
   #print('y range:', min_y_i, max_y_i)
   return pixels[min_x_i : max_x_i, min_y_i : max_y_i]
  
# Uniformly generates a random angle
def RandomAngle():
   return random.uniform(0, 2 * np.pi)
  
# Generates a uniform random float in [a, b] union [c, d].
# Assumes a < b < c < d, and only performs one sample.
def RandomDoubleInterval(a, b, c, d):
   interval_delta = c - b
   random_value = random.uniform(a, d - interval_delta)
   if (random_value > b):
      random_value += interval_delta
   return random_value
   
# Generates a uniform random float in the interval [left, right]
# with a middle portion of the interval removed.  The amount
# removed from the middle is given by middle_slice_ratio.
def RandomSlicedInterval(left, right, middle_slice_ratio):
   midpoint = 0.5 * (left + right)
   slice_width = middle_slice_ratio * (right - left)
   middle_slice_start = RoundToInt(midpoint - 0.5 * slice_width)
   middle_slice_end = RoundToInt(midpoint + 0.5 * slice_width)
   return RandomDoubleInterval(left, middle_slice_start - 1, middle_slice_end + 1, right)