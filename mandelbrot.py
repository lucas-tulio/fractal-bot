from __future__ import division
from PIL import Image, ImageDraw

width = 1280
height = 800

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

    real = (width / height) * (x - width / 2.0) / (0.5 * width)
    imaginary = (y - height / 2.0) / (0.5 * height)

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
      if newR * newR + newI * newI > 4.0:
        break

    draw.point([(x, y)], fill=(i, i, i))

    # Color, based on the number of iterations and the colorScheme
    #if(colorFactor[0] == 1 && colorFactor[1] == 1 && colorFactor[2] == 1) {
    #  pixels.putPixel(new Color(i, i, i));
    #} else {
    #  pixels.putPixel(new Color(i % colorFactor[0], i % colorFactor[1], i % colorFactor[2]));
    #}

  # Print progress
  if y % 10 == 0:
    print str((y / height) * 100) + "%"

# Save
im.save("test.png")































