from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from main import open, resize, grayscale, ascii, size, new_dims, remove_sessions


# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'heic', 'heif'}

# Initialize flask app
app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "/tmp/"
Session(app)

# Max session file limit for /tmp/ folder
FILES = 100

# Limiting size to 4.5 mb because of vercel server limit
app.config['MAX_CONTENT_LENGTH'] = 4.5 * 1024 * 1024


# List of character sets
DENSITY = ["@Ñ#W$9876543210ab?c!+=;:_-,.           ", "Wwli:,.  ",
            "@&%QWNM0gB$#DR8mHXKAUbGOpV4d9h6PkqwSE2]ayjxY5Zoen[ult13If}C{iF|(7J)vTLs?z/*cr!+<>;=^,_:'-.`                  ",
            "@%#*+=_:.  ", "$@B%8&WM#ahkbdpqwmZ0OQLCJUYXzocvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,*^`'.             ", "@#Oo*°.,  ",
            "¶@ØÆMåBNÊßÔR#8Q&mÃ0À$GXZA5ñk2S%±3Fz¢yÝCJf1t7ªLc¿+?(r/¤²!*;^:,'.`                       "]

# Check if uploaded file has allowed file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Error handler for invalid routes
@app.errorhandler(404)
def invalid_route(e):
    session['message'] = "Page not found"
    session['code'] = "404"
    return redirect("/error")

# Error handling for large payloads
@app.errorhandler(413)
def payload_too_large(e):
    session['message'] = "File size exceeds the server limit. Please submit image file of size less than 4.5 mb. This is implemented to reduce bandwidth and load on the server. I'm working on this, until then you can upload the screenshot of your original image as a workaround."
    session['code'] = 413
    return redirect("/error")


# Index route with GET and POST methods
@app.route("/", methods=["GET", "POST"])
def index():

    # When user reaches the page via post i.e., submitting the form
    if request.method == "POST":

        # Add global file variable
        global FILES

        # Check if file is uploaded through input form with name 'file'
        if 'file' not in request.files:
            session['message'] = "Hmmm suspecious. You think you're smart?"
            session['code'] = "203"
            return redirect("/error")

        # Get image file
        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            session['message'] = "How can you expect this to generate art for you if you don't submit an image file?"
            session['code'] = "204"
            return redirect("/error")

        # If filetype is not allowed
        elif not allowed_file(file.filename):
            session['message'] = "Upload jpg, jpeg, png, heic or heif image files only"
            session['code'] = "406"
            return redirect("/error")

        # Get index of character set
        set = request.form.get("density")

        # Check if user has selected character set radio
        if not set:
            session['message'] = "Select a character set"
            session['code'] = "204"
            return redirect("/error")
        
        # Get client browser-resolution and determine user-agent, max width and max height
        bwidth, bheight = request.form.get("resolution").split("x")
        if int(bwidth) < int(bheight):
            useragent = "mobile"
            max_width, max_height = int(int(bwidth) / 2), int(int(bheight) / 3.5)
        else:
            useragent = "pc"
            max_width, max_height = int(int(bwidth) / 2.5), int(int(bheight) / 4)

        # Open image, get its dimentions and calculate new image dimensions
        image = open(file)
        width, height = size(image)
        newimg_width, newimg_height = new_dims(width, height, max_width, max_height, useragent)

        # resize it and then convert to grayscale
        resized_image = resize(image, newimg_width, newimg_height)
        grayscale_img = grayscale(resized_image)

        # Make whole ascii string of grayscale image and calculate its length
        ascii_string = ascii(grayscale_img, DENSITY[int(set)])
        ascii_str_len = len(ascii_string)

        # Invert the image (density wise)
        ascii_string_rev = ascii(grayscale_img, DENSITY[int(set)][::-1])

        # Create new session for new user and remove old session files if greater than 100
        if "ascii" not in session:
            session['ascii'] = []
            session['invascii'] = []
            FILES -= 1
            if FILES == 0:
                FILES = 100
                remove_sessions()

        # If not a new user, clear ascii art from previous image
        else:
            session['ascii'].clear()
            session['invascii'].clear()

        # Slice the ascii string by width and append whole line to the lists
        for i in range(0, ascii_str_len, newimg_width):
            session['invascii'].append(ascii_string[i:i+newimg_width])
            session['ascii'].append(ascii_string_rev[i:i+newimg_width])

        return redirect("/ascii")

    else:
        return render_template("index.html")


# Render ascii page passing list of lines of art
@app.route("/ascii", methods=["GET", "POST"])
def art():
    if request.method == "POST":
        return redirect("/invascii")
    else:
        # If user has generated an image which is stored in its session, render art.html
        if "ascii" in session:
            return render_template("art.html", ascii=session['ascii'], button="Invert", action="/ascii")
        # Else if user has previously not generated any image, redirect to homepage
        else:
            return redirect("/")


# Render invert ascii page passing list of lines of art
@app.route("/invascii", methods=["GET", "POST"])
def inverse():
    if request.method == "POST":
        return redirect("/ascii")
    else:
        if "invascii" in session:
            return render_template("art.html", ascii=session['invascii'], button="Original", action="/invascii")
        else:
            return redirect("/")


# Render error page passing error message and error code
@app.route("/error")
def apology():
    
    # Redirect to error screen if there is really an error
    if 'code' in session:
        code = session['code']
        message = session['message']
        session.pop('code')
        session.pop('message')
        return render_template("error.html", code=code, error=message)
    
    # Else redirect to homepage
    else:
        return redirect("/")
