from PIL import Image, ImageDraw

# Create the image
im = Image.new("RGB", (400, 400))
draw = ImageDraw.Draw(im)

# Draw
draw.point([(0, 0)], fill=(255, 0, 0))

# Save
im.save("test.png")
