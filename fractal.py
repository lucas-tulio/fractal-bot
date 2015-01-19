from __future__ import division
from PIL import Image, ImageDraw
from random import random, randint, getrandbits, choice
from datetime import date
import sys, math, time, json

def getMandelbrotSmooth(mod, z, smoothDiv): # Mandelbrot smooth color value
  
  mod = math.sqrt(mod)
  lg = 0
  try:
    lg = math.log(math.log(mod))
  except:
    lg = 0
  return (z / smoothDiv) - lg / math.log(2)

def generateFractal(cr, ci):

  # Create the image
  im = Image.new("RGB", (width, height))
  draw = ImageDraw.Draw(im)

  # Set control
  newR = 0.0
  newI = 0.0
  oldR = 0.0
  oldI = 0.0
  smoothDiv = maxIterations / 255

  # Draw
  for y in range(0, height):
    for x in range(0, width):

      newR = (width / height) * (x - width / 2.0) / (0.5 * zoom * width) + offsetX + offsetXFix
      newI = (y - height / 2.0) / (0.5 * zoom * height) + offsetY

      if setType == "julia":
        smooth = math.exp(-math.sqrt(newR*newR + newI*newI))
      else:
        real = newR
        imaginary = newI
        newR = 0.0
        newI = 0.0
        oldR = 0.0
        oldI = 0.0

      # Start iterating
      for z in range(0, maxIterations):

        # Get the values of the previous iteration
        oldR = newR
        oldI = newI

        # Calculate the new real and imaginary parts
        if setType == "mandelbrot":
          cr = real
          ci = imaginary
        newR = (oldR * oldR) - (oldI * oldI) + cr
        newI = 2.0 * (oldR * oldI) + ci

        if setType == "julia":
          smooth += math.exp(-math.sqrt(newR*newR + newI*newI))

        # Exit condition
        mod = newR * newR + newI * newI
        if mod > 4.0:
          
          if setType == "mandelbrot":
            smooth = getMandelbrotSmooth(mod, z, smoothDiv)
          
          # Smooth has a value ranging from 0 to 255
          if setType == "mandelbrot":
            r = int(smooth * rColor * rBright * smoothDiv)
            g = int(smooth * gColor * gBright * smoothDiv)
            b = int(smooth * bColor * bBright * smoothDiv)
          else:
            r = int(smooth / smoothDiv * rColor * rBright)
            g = int(smooth / smoothDiv * gColor * gBright)
            b = int(smooth / smoothDiv * bColor * bBright)

          if invertColors:
            r = 255-r
            g = 255-g
            b = 255-b

          draw.point([(x, y)], fill=(r, g, b))
          break

        elif z == maxIterations - 1: # End of loop, draw inside the forms
          
          if (whiteCenter):
            r = int(255)
            g = int(255)
            b = int(255)
          else:
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
  im.save(fractalFileName)

isFractalOfTheDay = False
if len(sys.argv) == 2 and sys.argv[1] == "fotd":
  print "fractal of the day!"
  isFractalOfTheDay = True

# Read Parameters
fractalFileName = "fractal.png"
width = 640
height = 360

if isFractalOfTheDay:
  fractalFileName = "fotd.png"
  width = 1920
  height = 1080

# Get fractal parameters
f = open("sets.json")
data = json.load(f)
# setDetails = choice(data["sets"])
setDetails = data["sets"][8]

# Type
setType = setDetails["type"]
maxIterations = setDetails["maxIterations"]
print setType

# Offset
zoom = setDetails["zoom"]
offsetX = setDetails["offsetX"]
offsetY = setDetails["offsetY"]

# Offset fix
if setType == "mandelbrot":
  offsetXFix = -0.5
else:
  offsetXFix = 0.0

if setType == "julia":
  cr = setDetails["cr"]
  ci = setDetails["ci"]
else:
  cr = 0.0
  ci = 0.0

# Colors
invertColors = bool(getrandbits(1))
if setType == "mandelbrot":
  whiteCenter = True if randint(1, 10) == 1 else False
else:
  whiteCenter = False

rColor = random()
gColor = random()
bColor = random()

# Fix color to avoid full black or full white images
if rColor + gColor + bColor < 0.5:
  selected = randint(1, 3)
  if selected == 1:
    rColor = rColor + 0.5
  elif selected ==  2:
    gColor = gColor + 0.5
  else:
    bColor = bColor + 0.5

# Brightness
maxBrightness = 10
if zoom > 8000:
  maxBrightness = 3

rBright = randint(1, maxBrightness) # Min 1
gBright = randint(1, maxBrightness) # Min 1
bBright = randint(1, maxBrightness) # Min 1

# Go!
generateFractal(cr, ci)
