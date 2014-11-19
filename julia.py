from __future__ import division
from PIL import Image, ImageDraw
import sys

def getArg(argToGet, default):
  
  splitArgs = sys.argv[1:]
  for param in splitArgs:
    splitParam = param.split("=")
    paramName = splitParam[0]
    try:
      if paramName == argToGet:
        return float(splitParam[1])
    except:
      print "invalid arg"

  return default

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

      draw.point([(x, y)], fill=(i, i, i))

    # Print progress
    if y % 10 == 0:
      print str((y / height) * 100) + "%"

  # Save
  im.save("julia.png")

# Read Parameters
width = 400
height = 400

zoom = getArg("zoom", 1.0)
print "zoom: " + str(zoom)

xOffset = getArg("xOffset", 0)
print "xOffset: " + str(xOffset)

yOffset = getArg("yOffset", 0)
print "yOffset: " + str(yOffset)

cr = getArg("cr", -1.037)
print "cr = " + str(cr)

ci = getArg("ci", 0.17)
print "ci = " + str(ci)

generateFractal()
