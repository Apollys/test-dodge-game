import random
import numpy as np
import cv2
from timeit import default_timer as timer

import canvas
   
RESOLUTION = (600, 800)
   

def double_interval_random(a, b, c, d):
   ''' Assumes a < b < c < d
      Generates a uniform random float in [a, b] union [c, d]
      Only performs one sample
      '''
   interval_delta = c-d
   rand_val = random.uniform(a, d-interval_delta)
   if (rand_val > b):
      rand_val += interval_delta
   return rand_val
   
def main():

   print('Initializing canvas...')
   canv = canvas.Canvas(*RESOLUTION)
   canv.render(1)
   
   print('Drawing borders...')
   canv.draw_borders()
   canv.render_new_frame(1)
   
   NUM_CIRCLES = 10
   RADIUS_RANGE = (6, 10)
   VELOCITY_RANGE = (3, 7)
   border_zone = 20
   CX = RESOLUTION[1]/2
   CY = RESOLUTION[0]/2
   print('Adding', NUM_CIRCLES, 'circles...')
   for count in range(NUM_CIRCLES):
      radius = random.randint(*RADIUS_RANGE)
      # Leave space for the dodger to start in the middle
      cx = double_interval_random(border_zone + radius, CX-20, CX+20, RESOLUTION[1]-(border_zone + radius))
      cy = double_interval_random(border_zone + radius, CY-20, CY+20, RESOLUTION[0]-(border_zone + radius))
      velocity = random.uniform(*VELOCITY_RANGE)
      theta = random.uniform(0, 2*np.pi)
      vx = velocity * np.cos(theta)
      vy = velocity * np.sin(theta)
      canv.add_circle(cx, cy, radius, vx, vy)
   canv.render_new_frame(1)
   
   DODGER_SPEED = 4
   print('Adding dodger...')
   theta = random.uniform(0, 2*np.pi)
   speed = 4
   canv.create_dodger(CX, CY, theta, speed)
   
   canv.render_new_frame(0)
   
   # motion   
   SECONDS = 13
   EMPIRICAL_FPS = 64
   TOTAL_FRAMES = SECONDS*EMPIRICAL_FPS
   start = timer()
   for frame_num in range(TOTAL_FRAMES):
      canv.time_step()
      canv.render_new_frame(1)
   end = timer()
   
   print(TOTAL_FRAMES, "frames displayed in", end-start, "seconds")
   print("FPS:", TOTAL_FRAMES/(end-start))
   
   #print("Press any key to exit")
   #cv2.waitKey()
   
   cv2.destroyAllWindows()

if (__name__ == '__main__'):
   main()