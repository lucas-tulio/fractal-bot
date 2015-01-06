from __future__ import division
from PIL import Image, ImageDraw
import sys, math, random

def generateFractal():

  # Create the image
  im = Image.new("RGB", (width, height))
  draw = ImageDraw.Draw(im)

  # Set control
  maxIterations = 255
  smoothDiv = maxIterations / 255

  # Draw
  for y in range(0, height):
    for x in range(0, width):

      realP = (width / height) * (x - width / 2.0) / (0.5 * zoom * width) + offsetX - 0.5
      imaginaryP = (y - height / 2.0) / (0.5 * zoom * height) + offsetY

      # Zero the old real and imaginary parts
      newR = 0.0
      newI = 0.0
      oldR = 0.0
      oldI = 0.0
      
      # Start iterating
      for i in range(0, maxIterations):

        # Get the values of the previous iteration
        oldR = newR
        oldI = newI
        
        # Calculate the new real and imaginary parts
        newR = (oldR * oldR) - (oldI * oldI) + realP
        newI = 2.0 * oldR * oldI + imaginaryP
        
        # Exit condition
        mod = newR * newR + newI * newI
        if newR * newR + newI * newI > 4.0:
          
          # Color!
          mod = math.sqrt(mod)
          lg = 0
          try:
            lg = math.log(math.log(mod))
          except:
            lg = 0
          smooth = (i / smoothDiv) - lg / math.log(2)
          
          # Smooth has a value ranging from 0 to 255
          r = int(smooth * rColor * rBright * smoothDiv)
          g = int(smooth * gColor * gBright * smoothDiv)
          b = int(smooth * bColor * bBright * smoothDiv)

          if invertColors:
            r = 255-r
            g = 255-g
            b = 255-b

          draw.point([(x, y)], fill=(r, g, b))
          break

        elif i == maxIterations - 1: # End of loop, draw inside the forms
          r = int(255 * rColor * rBright)
          g = int(255 * gColor * gBright)
          b = int(255 * bColor * bBright)

          if invertColors:
            r = 255-r
            g = 255-g
            b = 255-b
          
          draw.point([(x, y)], fill=(r, g, b))

    # Print progress
    if y % 10 == 0:
      print str((y / height) * 100) + "%"

  # Save
  im.save("mandelbrot.png")

# Read Parameters
width = 1280
height = 720

zoom = 1.0

offsetX = 0.0
offsetY = 0.0

invertColors = False

rColor = random.random()
gColor = random.random()
bColor = random.random()
rBright = 10 # Min 1
gBright = 10 # Min 1
bBright = 10 # Min 1

generateFractal()
