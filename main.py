from PIL import Image
from math import floor


# Open image
def open(image):
    return Image.open(image)

# Get width of image
def width(image):
    return image.width

# Resize image maintaining aspect ratio
def resize(image, width):

    # width_percent = (new_width/float(image.size[0]))
    # new_height = int((float(image.size[1])*float(width_percent)))
    # return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    orig_width, orig_height = image.size
    r = orig_height / orig_width

    # The ASCII character glyphs are taller than they are wide. Maintain the aspect
    # ratio by reducing the image height.
    height = int(width * r * 0.6)
    return image.resize((width, height), Image.Resampling.LANCZOS)

# Convert image to grayscale
def grayscale(image):
    return image.convert("L")

# Convert pixel string to ascii character string
def ascii(image, den):

    # Get pixels of image
    pixels = image.getdata()
    ascii_string = ""

    # For each pixel, map its value to ascii character and append it to the ascii_string
    for pixel in pixels:
        ascii_string += den[map(pixel, 0, 255, 0, len(den) - 1)]

    return ascii_string

# Maps value from one range to a value in another range
def map(value, start1, stop1, start2, stop2):
    OldRange = (stop1 - start1)
    NewRange = (stop2 - start2)
    mappedValue = (((value - start1) * NewRange) / OldRange) + start2
    return floor(mappedValue)
