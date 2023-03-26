from PIL import Image
from math import floor
from pillow_heif import register_heif_opener
# from os import remove, listdir, path
# from time import time


# used to open and work with helf/heic images in PIL
register_heif_opener()

# Open image
def open(image):
    return Image.open(image)

# Rotate image counter-clockwise by an angle
def rotate(image, angle):
    return image.rotate(angle, expand = 1)

# Calculate new dimentions of the image, maintaining aspect ratio
def new_dims(w, h, mw, mh, agent):
    # aspect ratio
    r = h / w

    # The ASCII character glyphs are taller than they are wide. Maintain the aspect
    # ratio by reducing the image height
    nw = mw
    nh = int(nw * r * 0.6)

    # If width or height is greater than its max value,
    # limit it to the max value and calculate other dimension
    if agent == "mobile":
        if nh > mh:
            nh = mh
            nw = int(nh / (r * 0.6))
    else:
        if w > h:
            if nh > mh:
                nh = mh
                nw = int(nh / (r * 0.55))
        else:
            nh = mh
            nw = int(nh / (r * 0.55))
    return nw, nh

# Get size of image
def size(image):
    return image.size

# Resize image maintaining aspect ratio
def resize(image, width, height):

    # width_percent = (new_width/float(image.size[0]))
    # new_height = int((float(image.size[1])*float(width_percent)))
    # return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # orig_width, orig_height = image.size
    # r = orig_height / orig_width

    # The ASCII character glyphs are taller than they are wide. Maintain the aspect
    # ratio by reducing the image height.
    # height = int(width * r * 0.6)

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

# Remove sessions in /tmp/ folder
# def remove_sessions():
#     dir_path = '/tmp/'

    # Get the current time in seconds
    # current_time = time()

    # Iterate through all files in the /tmp/ folder
    # for file_name in listdir(dir_path):
    #     file_path = path.join(dir_path, file_name)
        
        # Check and delete file if it has no extension and was created more than 10 mins ago
        # if path.isfile(file_path) and '.' not in file_name:
        #     if current_time - path.getctime(file_path) > 600:
        #         remove(file_path)