from dotenv import load_dotenv
from inky import InkyPHAT
import math
import os
from PIL import Image, ImageOps
import requests
import sys
from twilio.rest import Client

# Initialize constants
BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))
#INKY_DISPLAY_RATIO = inky_display.height / inky_display.width
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
TWILIO_BASE_URI = "https://api.twilio.com"

# Downsample method
def recolor(img):
    img = image.convert('RGB')
    inky_img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
    for y in range(inky_display.HEIGHT):
        for x in range(inky_display.WIDTH):
            pixelMap = img.load()
            if pixelMap[x,y] == (128,128,128) or pixelMap[x,y] == (255,255,255):
                inky_img.putpixel((x,y), (255,255,255))
            elif pixelMap[x,y] == (0, 0, 0):
                inky_img.putpixel((x,y), (0,0,0))
            else:
                inky_img.putpixel((x,y), (255,255,0))
    return inky_img

# Get latest image
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
def date(msg):
    return msg.date_sent
recentmsgs = client.messages.list()
recentmsgs.sort(key=date, reverse=True)
currentimage = "none"
for msg in recentmsgs:
    if msg.sid[:1] == "M" and msg.to == TWILIO_PHONE_NUMBER:
        message = client.messages(msg.sid).fetch()
        break
allimgs = client.messages(message.sid).media.list()
for img in allimgs:
    imageuri = (TWILIO_BASE_URI + str(img.uri)).strip(".json'").strip("u'")
print(imageuri)
try:
    response = requests.get(imageuri, stream=True).raw
except requests.exceptions.RequestException as e:  
    sys.exit(1)

# Create inkyPHAT image
inky_display = InkyPHAT("yellow")

# Resize and crop incoming image
originalimage = Image.open(response)
originalimageW = float(img.size[0])
originalimageH = float(img.size[1])
imgRatio = originalimageW/originalimageH
if (imgRatio >= inky_display.HEIGHT/inky_display.WIDTH):
    originalimage = originalimage.resize((inky_display.WIDTH, int((1/imgRatio)*inky_display.WIDTH)), resample=Image.BILINEAR) 
    originalimage = originalimage.crop((0, 0, inky_display.WIDTH, inky_display.HEIGHT))
else:
    originalimage = originalimage.resize((int(imgRatio*inky_display.HEIGHT), inky_display.HEIGHT), resample=Image.BILINEAR)
    originalimage = originalimage.crop((originalimage.size[0]-inky_display.WIDTH)/2, 0, (originalimage.size[0]-inky_display.WIDTH)/2+inky_display.WIDTH, inky_display.HEIGHT)
originalimage = originalimage.rotate(90, expand=1)

# Downsample original image
originalimage = ImageOps.posterize(originalimage, bits=1)
convertedimage = recolor(originalimage)

# Display on inkyPHAT
inky_display.set_image(convertedimage)
inky_display.show()