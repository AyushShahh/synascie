# ASCII Art <img src="static/favicon-32x32.png">
Convert any image into ASCII character art.

Video demo: [Watch on YouTube](https://www.youtube.com/watch?v=kvW-cWD7sYY)

<img src="static/asciidog.JPG" height=300>

## Explanation
ASCII Art is a website that converts any image into ASCII character art. Basically what it means is that it generates an image made of ASCII characters (characters like !@#$%^&*_-+= etc) based on the character set you have chosen.

#### What is ASCII Art?
ASCII art is a graphic design technique that uses computers for presentation and consists of pictures pieced together from
different ASCII Characters. It was invented, in large part, because early printers often lacked graphics ability and
thus, characters were used in place of graphic marks.

#### How is an image converted into ASCII character art?
First of all, the image is resized to a smaller size and is then converted to grayscale.
The reason behind converting to grayscale is that we can get the darkness of the pixel (amount of blackness or whiteness)
and then we can map each pixel to an ASCII character according to its density (for example 'Ñ' for the darkest pixel and "&nbsp;`&nbsp;" or "&nbsp;&nbsp;" (whitespace) for the brightest pixel). Different ASCII character sets can be used.

## Tech Stack
- Python
- HTML
- CSS
- JavaScript
- Jinja templating

## Libraries Used
- PIL - For image processing
- math - For using math functions
- Flask - For using flask features

## Explaining the code
There are two python files, _main.py_ and _app.py_. _main.py_ contains functions for image processing while _app.py_ configures flask and defines route functions. HTML files are in the templates folder. _layout.html_ is the template file and other HTML files are the extensions of it. Images, CSS file and favicons are in the static folder.

#### main.py
Open and width functions are for opening an image file and getting the width of an image file respectively.

Resize function is for resizing the image file with maintaining the aspect ratio. A normal image file consists of thousands of pixels. Resizing to lower amount is better for performance and there are other benefits too.

Grayscale function converts an image to grayscale. The reason for turning to grayscale is that we can get the darkness value of each pixel and then we can perform operations on the image based on this darkness value.

Ascii function gets all pixel values from the grayscale image and maps an ascii character from the chosen character set to that pixel and stores the whole art in a string. For example the dakrest pixel might map to @ and the brightest pixel gets mapped to " " (whitespace).

Map function has all the math for mapping. Mapping requires converting a value from one range to another.

#### app.py
Flask is configured, list of character sets is defined and initialising lists which will store each line of generated ascii art (normal and inverse).

Error handler for invalid routes is defined and function for checking allowed filename is defined.

"/" route error checks input conditions and then performs operations to get ascii string of character art. Then each line of length equal to width of grayscale image is appended to the list and the list.

Error function passes message and code to html.
