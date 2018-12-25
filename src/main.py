import random
import numpy as np
import cv2
from timeit import default_timer as timer

import math_util
import canvas

# Constants
kResolution = (700, 500)  # 800, 600

# Game parameters
kDodgerSpeed = 200  # 200
kDodgerTurningRate = kDodgerSpeed / 2857.142857  # 0.07
kNumCircles = 10  # 16
kCircleRadiusRange = (6, 10)
kCircleVelocityRange = (2, 5)
kMiddleSpawnBufferRatio = 0.3

# Debugging constant
kPause = False
   
def main():
   # Initialize canvas
   print('Initializing canvas...')
   canvas_object = canvas.Canvas(*kResolution)
   canvas_object.RenderSingleFrame(kPause)
   # Draw borders
   print('Drawing borders...')
   canvas_object.DrawBorders()
   canvas_object.RenderSingleFrame(kPause)
   # Draw circles
   print('Adding', kNumCircles, 'circles...')
   for count in range(kNumCircles):
      radius = random.randint(*kCircleRadiusRange)
      # Leave space for the dodger to start in the middle
      xmin, xmax = canvas_object.playable_area_xrange_
      ymin, ymax = canvas_object.playable_area_yrange_
      cx = math_util.RandomSlicedInterval(xmin, xmax, kMiddleSpawnBufferRatio)
      cy = math_util.RandomSlicedInterval(ymin, ymax, kMiddleSpawnBufferRatio)
      velocity = random.uniform(*kCircleVelocityRange)
      theta = math_util.RandomAngle()
      vx = velocity * np.cos(theta)
      vy = velocity * np.sin(theta)
      canvas_object.AddCircle(cx, cy, radius, vx, vy)
   canvas_object.RenderSingleFrame(kPause)
   # Draw dodger
   print('Adding dodger...')
   xmin, xmax = canvas_object.playable_area_xrange_
   ymin, ymax = canvas_object.playable_area_yrange_
   cx = math_util.RoundToInt(0.5 * (xmin + xmax))
   cy = math_util.RoundToInt(0.5 * (ymin + ymax))
   theta = math_util.RandomAngle()
   canvas_object.CreateDodger(cx, cy, theta, kDodgerSpeed, kDodgerTurningRate)
   canvas_object.RenderSingleFrame(pause=True)
   # Motion
   #SECONDS = 15
   #EMPIRICAL_FPS = 64
   #TOTAL_FRAMES = SECONDS*EMPIRICAL_FPS
   canvas_object.MainGameLoop()

if (__name__ == '__main__'):
   main()