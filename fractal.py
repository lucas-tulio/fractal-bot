from __future__ import division
from PIL import Image, ImageDraw
from random import random, randint, getrandbits, choice
import math, json

class Fractal:

  def __init__(self):
    pass

  def _define_parameters(self):
    
    # Get fractal parameters
    f = open("sets.json")
    data = json.load(f)
    set_details = choice(data["sets"])

    # Type
    self.set_type = set_details["type"]
    self.max_iterations = set_details["maxIterations"]
    print(self.set_type)

    # Offset
    self.zoom = set_details["zoom"]
    self.offset_x = set_details["offsetX"]
    self.offset_y = set_details["offsetY"]

    # Offset fix
    if self.set_type == "mandelbrot":
      self.offset_x_fix = -0.5
    else:
      self.offset_x_fix = 0.0

    if self.set_type == "julia":
      self.cr = set_details["cr"]
      self.ci = set_details["ci"]
    else:
      self.cr = 0.0
      self.ci = 0.0

    # Colors
    self.invert_colors = bool(getrandbits(1))
    if self.set_type == "mandelbrot":
      self.white_center = True if randint(1, 10) == 1 else False
    else:
      self.white_center = False

    self.r_color = random()
    self.g_color = random()
    self.b_color = random()

    # Fix color to avoid full black or full white images
    if self.r_color + self.g_color + self.b_color < 0.5:
      selected = randint(1, 3)
      if selected == 1:
        self.r_color = self.r_color + 0.5
      elif selected ==  2:
        self.g_color = self.g_color + 0.5
      else:
        self.b_color = self.b_color + 0.5

    # Brightness
    self.max_brightness = 10
    if self.zoom > 8000:
      self.max_brightness = 3

    self.r_bright = randint(1, self.max_brightness) # Min 1
    self.g_bright = randint(1, self.max_brightness) # Min 1
    self.b_bright = randint(1, self.max_brightness) # Min 1

  def _get_mandelbrot_smooth(self, mod, z, smooth_div): # Mandelbrot smooth color value
    
    mod = math.sqrt(mod)
    lg = 0
    try:
      lg = math.log(math.log(mod))
    except:
      lg = 0
    return (z / smooth_div) - lg / math.log(2)

  def generate(self, fotd=False):

    # Fractal of the day?
    if fotd:
      print("Fractal of the Day!")
      fractal_file_name = "fotd.png"
      width = 1920
      height = 1080
    else:
      fractal_file_name = "fractal.png"
      width = 960
      height = 540

    self._define_parameters()

    # Create the image
    im = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(im)

    # Set control
    newR = 0.0
    newI = 0.0
    oldR = 0.0
    oldI = 0.0
    smooth_div = self.max_iterations / 255

    # Draw
    for y in range(0, height):
      for x in range(0, width):

        newR = (width / height) * (x - width / 2.0) / (0.5 * self.zoom * width) + self.offset_x + self.offset_x_fix
        newI = (y - height / 2.0) / (0.5 * self.zoom * height) + self.offset_y

        if self.set_type == "julia":
          smooth = math.exp(-math.sqrt(newR*newR + newI*newI))
        else:
          real = newR
          imaginary = newI
          newR = 0.0
          newI = 0.0
          oldR = 0.0
          oldI = 0.0

        # Start iterating
        for z in range(0, self.max_iterations):

          # Get the values of the previous iteration
          oldR = newR
          oldI = newI

          # Calculate the new real and imaginary parts
          if self.set_type == "mandelbrot":
            self.cr = real
            self.ci = imaginary
          newR = (oldR * oldR) - (oldI * oldI) + self.cr
          newI = 2.0 * (oldR * oldI) + self.ci

          if self.set_type == "julia":
            smooth += math.exp(-math.sqrt(newR*newR + newI*newI))

          # Exit condition
          mod = newR * newR + newI * newI
          if mod > 4.0:
            
            if self.set_type == "mandelbrot":
              smooth = self._get_mandelbrot_smooth(mod, z, smooth_div)
            
            # Smooth has a value ranging from 0 to 255
            if self.set_type == "mandelbrot":
              r = int(smooth * self.r_color * self.r_bright * smooth_div)
              g = int(smooth * self.g_color * self.g_bright * smooth_div)
              b = int(smooth * self.b_color * self.b_bright * smooth_div)
            else:
              r = int(smooth / smooth_div * self.r_color * self.r_bright)
              g = int(smooth / smooth_div * self.g_color * self.g_bright)
              b = int(smooth / smooth_div * self.b_color * self.b_bright)

            if self.invert_colors:
              r = 255-r
              g = 255-g
              b = 255-b

            draw.point([(x, y)], fill=(r, g, b))
            break

          elif z == self.max_iterations - 1: # End of loop, draw inside the forms
            
            if (self.white_center):
              r = int(255)
              g = int(255)
              b = int(255)
            else:
              r = int(255 * self.r_color * self.r_bright)
              g = int(255 * self.g_color * self.g_bright)
              b = int(255 * self.b_color * self.b_bright)

            if self.invert_colors:
              r = 255-r
              g = 255-g
              b = 255-b
            
            draw.point([(x, y)], fill=(r, g, b))

      # Print progress
      if y % 10 == 0:
        print(str((y / height) * 100) + "%")

    # Save
    im.save(fractal_file_name)
    print("Done. File " + str(fractal_file_name) + " saved")
