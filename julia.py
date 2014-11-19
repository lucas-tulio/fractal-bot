from __future__ import division
from PIL import Image, ImageDraw

width = 400
height = 400

# Parameters
zoom = 2.4
xOffset = 0
yOffset = -0.6

# Create the image
im = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(im)

# Set control
cr = -1.037
ci = 0.17
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































