from flask import Flask, redirect, render_template, request
from main import open, resize, grayscale, ascii, size, new_dims


# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'heic', 'heif'}

app = Flask(__name__)

# Initialising lists which will store each line of generated ascii art
ASCII_ART = []
ASCII_ART_INV = []

# List of character sets
DENSITY = ["@Ñ#W$9876543210ab?c!+=;:_-,.           ", "Wwli:,.  ",
            "@&%QWNM0gB$#DR8mHXKAUbGOpV4d9h6PkqwSE2]ayjxY5Zoen[ult13If}C{iF|(7J)vTLs?z/*cr!+<>;=^,_:'-.`                  ",
            "@%#*+=_:.  ", "$@B%8&WM#ahkbdpqwmZ0OQLCJUYXzocvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,*^`'.             ", "@#Oo*°.,  ",
            "¶@ØÆMåBNÊßÔR#8Q&mÃ0À$GXZA5ñk2S%±3Fz¢yÝCJf1t7ªLc¿+?(r/¤²!*;^:,'.`                       "]

# Errors
MESSAGE = ""
CODE = ""


# Check if uploaded file has allowed file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Error handler for invalid routes
@app.errorhandler(404)
def invalid_route(e):
    global MESSAGE
    global CODE
    MESSAGE = "Not found"
    CODE = "404"
    return redirect("/error")


# Index route with GET and POST methods
@app.route("/", methods=["GET", "POST"])
def index():

    # When user reaches the page via post i.e., submitting the form
    if request.method == "POST":

        # Add global variables
        global MESSAGE
        global CODE

        # Check if file is uploaded through input form with name 'file'
        if 'file' not in request.files:
            MESSAGE = "Hmmm suspecious"
            CODE = "203"
            return redirect("/error")

        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            MESSAGE = "No content. Please submit an image file"
            CODE = "204"
            return redirect("/error")

        # If filetype is not allowed
        elif not allowed_file(file.filename):
            MESSAGE = "Please upload jpg, jpeg, png, heic or heif image files"
            CODE = "406"
            return redirect("/error")

        # Get index of character set
        set = request.form.get("density")

        # Check if user has selected character set radio
        if not set:
            MESSAGE = "Please select a character set"
            CODE = "204"
            return redirect("/error")
        
        # Get client browser-resolution and determine user-agent, max width and max height
        bwidth, bheight = request.form.get("resolution").split("x")
        if int(bwidth) < int(bheight):
            useragent = "mobile"
            max_width, max_height = int(int(bwidth) / 2), int(int(bheight) / 3.5)
        else:
            useragent = "pc"
            max_width, max_height = int(int(bwidth) / 2.5), int(int(bheight) / 4)
        

        # Open image, get its dimentions and new image dimensions
        image = open(file)
        width, height = size(image)
        newimg_width, newimg_height = new_dims(width, height, max_width, max_height, useragent)

        # resize it and then convert to grayscale
        resized_image = resize(image, newimg_width, newimg_height)
        grayscale_img = grayscale(resized_image)

        # Get whole ascii string of grayscale image and its length
        ascii_string = ascii(grayscale_img, DENSITY[int(set)])
        ascii_str_len = len(ascii_string)

        # Invert the image (density wise)
        ascii_string_rev = ascii(grayscale_img, DENSITY[int(set)][::-1])

        # Clear previous list of generated ascii art
        ASCII_ART.clear()
        ASCII_ART_INV.clear()

        # Slice the ascii string by width and append whole line to the lists
        for i in range(0, ascii_str_len, newimg_width):
            ASCII_ART_INV.append(ascii_string[i:i+newimg_width])
            ASCII_ART.append(ascii_string_rev[i:i+newimg_width])

        return redirect("/ascii")

    else:
        return render_template("index.html")


# Render ascii page passing list of lines of art
@app.route("/ascii", methods=["GET", "POST"])
def art():
    if request.method == "POST":
        return redirect("/invascii")
    else:
        return render_template("art.html", ascii=ASCII_ART)


# Render invert ascii page passing list of lines of art
@app.route("/invascii", methods=["GET", "POST"])
def inverse():
    if request.method == "POST":
        return redirect("/ascii")
    else:
        return render_template("invart.html", ascii=ASCII_ART_INV)


# Render error page passing error message and error code
@app.route("/error")
def apology():
    return render_template("error.html", code=CODE, error=MESSAGE)
