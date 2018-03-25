import random
import numpy as np
import cv2
from timeit import default_timer as timer

import canvas

# resolution: (x, y)
RESOLUTION = (800, 600)
   

def double_interval_random(a, b, c, d):
   ''' Assumes a < b < c < d
      Generates a uniform random float in [a, b] union [c, d]
      Only performs one sample
      '''
   interval_delta = c-b
   rand_val = random.uniform(a, d-interval_delta)
   if (rand_val > b):
      rand_val += interval_delta
   return rand_val
   
def main():

   PAUSE=False

   print('Initializing canvas...')
   canv = canvas.Canvas(*RESOLUTION)
   canv.render_single_frame(pause=PAUSE)
   
   print('Drawing borders...')
   canv.draw_borders()
   canv.render_single_frame(pause=PAUSE)
   
   NUM_CIRCLES = 16
   print('Adding', NUM_CIRCLES, 'circles...')
   RADIUS_RANGE = (6, 10)
   VELOCITY_RANGE = (2, 5)
   border_zone = 20
   CX = RESOLUTION[1]/2
   CY = RESOLUTION[0]/2
   for count in range(NUM_CIRCLES):
      radius = random.randint(*RADIUS_RANGE)
      # Leave space for the dodger to start in the middle
      SPACE = 70
      cx = double_interval_random(border_zone + radius, CX-SPACE, CX+SPACE, RESOLUTION[1]-(border_zone + radius))
      cy = double_interval_random(border_zone + radius, CY-SPACE, CY+SPACE, RESOLUTION[0]-(border_zone + radius))
      velocity = random.uniform(*VELOCITY_RANGE)
      theta = random.uniform(0, 2*np.pi)
      vx = velocity * np.cos(theta)
      vy = velocity * np.sin(theta)
      canv.add_circle(cx, cy, radius, vx, vy)
   canv.render_single_frame(pause=PAUSE)
   
   DODGER_SPEED = 200
   print('Adding dodger...')
   theta = random.uniform(0, 2*np.pi)
   canv.create_dodger(CX, CY, theta, DODGER_SPEED)
   canv.render_single_frame(pause=True)
   
   # motion
   SECONDS = 15
   EMPIRICAL_FPS = 64
   TOTAL_FRAMES = SECONDS*EMPIRICAL_FPS
   canv.main_game_loop()

if (__name__ == '__main__'):
   main()