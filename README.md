# ASCII Art <img src="static/favicons/favicon-32x32.png">
Convert any image into ASCII character art.

Video demo: [Watch on YouTube](https://www.youtube.com/watch?v=kvW-cWD7sYY)

<img src="static/asciidog.JPG" height=300>

ASCII Art is a website that converts any image into ASCII character art. Basically what it means is that it generates an image made of ASCII characters (characters like !@#$%^&*_-+= etc) based on the character set you have chosen.

# Local development
Clone this repository
``` terminal
git clone https://github.com/AyushShahh/ASCII-Art.git
```
Change your working directory to this folder or open terminal in this directory's location and run
```terminal
pip install -r requirements.txt
```
Start flask development server
``` terminal
flask --debug run --host=0.0.0.0
```

## Tech Stack
- Python
- HTML
- CSS
- JavaScript
- Ajax
- Jinja templating

## Libraries Used
- PIL - For image processing
- Flask - For using flask features
- pillow_heif - Adding support for heic and heif images
- flask_sessions - For adding browser sessions