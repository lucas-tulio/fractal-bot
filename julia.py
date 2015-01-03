from __future__ import division
from PIL import Image, ImageDraw
import sys, random

def generateFractal():

  # Create the image
  im = Image.new("RGB", (width, height))
  draw = ImageDraw.Draw(im)

  # Set control
  newR = 0.0
  newI = 0.0
  oldR = 0.0
  oldI = 0.0
  maxIterations = 255

  # Draw
  for y in range(0, height):
    for x in range(0, width):

      newR = (width / height) * (x - width / 2.0) / (0.5 * zoom * width) + xOffset
      newI = (y - height / 2.0) / (0.5 * zoom * height) + yOffset

      # Start iterating
      for i in range(0, maxIterations):

        # Get the values of the previous iteration
        oldR = newR
        oldI = newI
        
        # Calculate the new real and imaginary parts
        newR = (oldR * oldR) - (oldI * oldI) + cr
        newI = 2.0 * oldR * oldI + ci
        
        # Exit condition
        if newR * newR + newI * newI > 4.0:
          break

      r = int(i % rColor)
      g = int(i % gColor)
      b = int(i % bColor)
      draw.point([(x, y)], fill=(r, g, b))

    # Print progress
    if y % 10 == 0:
      print str((y / height) * 100) + "%"

  # Save
  im.save("julia.png")

# Read Parameters
width = 900
height = 600

zoom = 3.0

xOffset = 0
yOffset = 0

cr = -0.8
ci = 0.156

rColor = random.randint(0, 255)
gColor = random.randint(0, 255)
bColor = random.randint(0, 255)

generateFractal()
