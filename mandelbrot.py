from __future__ import division
from PIL import Image, ImageDraw
import sys, math, random

def generateFractal():

  # Create the image
  im = Image.new("RGB", (width, height))
  draw = ImageDraw.Draw(im)

  # Set control
  real = 0.0
  imaginary = 0.0
  newR = 0.0
  newI = 0.0
  oldR = 0.0
  oldI = 0.0
  maxIterations = 255

  # Draw
  for y in range(0, height):
    for x in range(0, width):

      real = (width / height) * (x - width / 2.0) / (0.5 * zoom * width) + offsetX - 0.5
      imaginary = (y - height / 2.0) / (0.5 * zoom * height) + offsetY

      # Zero the new and old real and imaginary parts
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
        newR = (oldR * oldR) - (oldI * oldI) + real
        newI = 2.0 * oldR * oldI + imaginary
        
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
          smooth = i - lg / math.log(2)

          # Smooth has a value ranging from 0 to 255
          r = int((smooth * rColor))
          g = int((smooth * gColor))
          b = int((smooth * bColor))
          draw.point([(x, y)], fill=(r, g, b))
          break

        elif i == maxIterations - 1: # Draw inside the forms
          r = int(255)
          g = int(255)
          b = int(255)
          draw.point([(x, y)], fill=(r, g, b))

    # Print progress
    if y % 10 == 0:
      print str((y / height) * 100) + "%"

  # Save
  im.save("mandelbrot.png")

# Read Parameters
width = 1360
height = 768

zoom = 1.0

offsetX = 0
offsetY = 0

rColor = random.random()
gColor = random.random()
bColor = random.random()

generateFractal()
