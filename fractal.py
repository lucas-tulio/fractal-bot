from __future__ import division
from PIL import Image, ImageDraw
from random import random, randint, getrandbits, choice
from datetime import date
import sys, math, time, json

class Fractal:

  def __init__(self):
    pass

  def _defineParameters(self):
    
    # Get fractal parameters
    f = open("sets.json")
    data = json.load(f)
    setDetails = choice(data["sets"])

    # Type
    self.setType = setDetails["type"]
    self.maxIterations = setDetails["maxIterations"]
    print self.setType

    # Offset
    self.zoom = setDetails["zoom"]
    self.offsetX = setDetails["offsetX"]
    self.offsetY = setDetails["offsetY"]

    # Offset fix
    if self.setType == "mandelbrot":
      self.offsetXFix = -0.5
    else:
      self.offsetXFix = 0.0

    if self.setType == "julia":
      self.cr = setDetails["cr"]
      self.ci = setDetails["ci"]
    else:
      self.cr = 0.0
      self.ci = 0.0

    # Colors
    self.invertColors = bool(getrandbits(1))
    if self.setType == "mandelbrot":
      self.whiteCenter = True if randint(1, 10) == 1 else False
    else:
      self.whiteCenter = False

    self.rColor = random()
    self.gColor = random()
    self.bColor = random()

    # Fix color to avoid full black or full white images
    if self.rColor + self.gColor + self.bColor < 0.5:
      selected = randint(1, 3)
      if selected == 1:
        self.rColor = self.rColor + 0.5
      elif selected ==  2:
        self.gColor = self.gColor + 0.5
      else:
        self.bColor = self.bColor + 0.5

    # Brightness
    self.maxBrightness = 10
    if self.zoom > 8000:
      self.maxBrightness = 3

    self.rBright = randint(1, self.maxBrightness) # Min 1
    self.gBright = randint(1, self.maxBrightness) # Min 1
    self.bBright = randint(1, self.maxBrightness) # Min 1

  def _getMandelbrotSmooth(self, mod, z, smoothDiv): # Mandelbrot smooth color value
    
    mod = math.sqrt(mod)
    lg = 0
    try:
      lg = math.log(math.log(mod))
    except:
      lg = 0
    return (z / smoothDiv) - lg / math.log(2)

  def generate(self, fotd=False):

    # Fractal of the day?
    if fotd:
      print "Fractal of the Day!"
      fractalFileName = "fotd.png"
      width = 1920
      height = 1080
    else:
      fractalFileName = "fractal.png"
      width = 640
      height = 360

    self._defineParameters()

    # Create the image
    im = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(im)

    # Set control
    newR = 0.0
    newI = 0.0
    oldR = 0.0
    oldI = 0.0
    smoothDiv = self.maxIterations / 255

    # Draw
    for y in range(0, height):
      for x in range(0, width):

        newR = (width / height) * (x - width / 2.0) / (0.5 * self.zoom * width) + self.offsetX + self.offsetXFix
        newI = (y - height / 2.0) / (0.5 * self.zoom * height) + self.offsetY

        if self.setType == "julia":
          smooth = math.exp(-math.sqrt(newR*newR + newI*newI))
        else:
          real = newR
          imaginary = newI
          newR = 0.0
          newI = 0.0
          oldR = 0.0
          oldI = 0.0

        # Start iterating
        for z in range(0, self.maxIterations):

          # Get the values of the previous iteration
          oldR = newR
          oldI = newI

          # Calculate the new real and imaginary parts
          if self.setType == "mandelbrot":
            self.cr = real
            self.ci = imaginary
          newR = (oldR * oldR) - (oldI * oldI) + self.cr
          newI = 2.0 * (oldR * oldI) + self.ci

          if self.setType == "julia":
            smooth += math.exp(-math.sqrt(newR*newR + newI*newI))

          # Exit condition
          mod = newR * newR + newI * newI
          if mod > 4.0:
            
            if self.setType == "mandelbrot":
              smooth = self._getMandelbrotSmooth(mod, z, smoothDiv)
            
            # Smooth has a value ranging from 0 to 255
            if self.setType == "mandelbrot":
              r = int(smooth * self.rColor * self.rBright * smoothDiv)
              g = int(smooth * self.gColor * self.gBright * smoothDiv)
              b = int(smooth * self.bColor * self.bBright * smoothDiv)
            else:
              r = int(smooth / smoothDiv * self.rColor * self.rBright)
              g = int(smooth / smoothDiv * self.gColor * self.gBright)
              b = int(smooth / smoothDiv * self.bColor * self.bBright)

            if self.invertColors:
              r = 255-r
              g = 255-g
              b = 255-b

            draw.point([(x, y)], fill=(r, g, b))
            break

          elif z == self.maxIterations - 1: # End of loop, draw inside the forms
            
            if (self.whiteCenter):
              r = int(255)
              g = int(255)
              b = int(255)
            else:
              r = int(255 * self.rColor * self.rBright)
              g = int(255 * self.gColor * self.gBright)
              b = int(255 * self.bColor * self.bBright)

            if self.invertColors:
              r = 255-r
              g = 255-g
              b = 255-b
            
            draw.point([(x, y)], fill=(r, g, b))

      # Print progress
      if y % 10 == 0:
        print str((y / height) * 100) + "%"

    # Save
    im.save(fractalFileName)
    print "Done. File " + str(fractalFileName) + " saved"
