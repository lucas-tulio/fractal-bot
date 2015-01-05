from __future__ import division
from PIL import Image, ImageDraw
import sys, random, math, colorsys

def generateFractal():

  # Create the image
  im = Image.new("RGB", (width, height))
  draw = ImageDraw.Draw(im)

  # Set control
  newR = 0.0
  newI = 0.0
  oldR = 0.0
  oldI = 0.0
  maxIterations = 1024

  # Draw
  for y in range(0, height):
    for x in range(0, width):

      newR = (width / height) * (x - width / 2.0) / (0.5 * zoom * width) + xOffset
      newI = (y - height / 2.0) / (0.5 * zoom * height) + yOffset
      smooth = math.exp(-math.sqrt(newR*newR + newI*newI))

      # Start iterating
      for i in range(0, maxIterations):

        # Get the values of the previous iteration
        oldR = newR
        oldI = newI
        
        # Calculate the new real and imaginary parts
        newR = (oldR * oldR) - (oldI * oldI) + cr
        newI = 2.0 * oldR * oldI + ci

        smooth += math.exp(-math.sqrt(newR*newR + newI*newI))
        
        # Exit condition
        if newR*newR + newI*newI > 4.0:
          break

        r = int(smooth * rColor * (i / 4))
        g = int(smooth * gColor * (i / 4))
        b = int(smooth * bColor * (i / 4))
        draw.point([(x, y)], fill=(r, g, b))

    # Print progress
    if y % 10 == 0:
      print str((y / height) * 100) + "%"

  # Save
  im.save("julia.png")

# Read Parameters
width = 1360
height = 768

zoom = 1.0

xOffset = 0
yOffset = 0

cr = -0.1
ci = 0.651

rColor = random.random()
gColor = random.random()
bColor = random.random()

generateFractal()
