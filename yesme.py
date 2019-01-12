from dotenv import load_dotenv
import math
import os
from PIL import Image, ImageOps
import requests
import sys
from twilio.rest import Client

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)
TWILIO_BASE_URI = "https://api.twilio.com"
INKY_HEIGHT = 212.00
INKY_WIDTH = 104.00
INKY_RATIO = INKY_HEIGHT/INKY_WIDTH

def recolor(img):
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            pixelMap = img.load()
            if pixelMap[x,y] == (128,128,128) or pixelMap[x,y] == (255,255,255):
                pixelMap[x,y] = (255,255,255)
            elif pixelMap[x,y] == (0, 0, 0):
                pass
            else:
                pixelMap[x,y] = (255,255,0)

some_messages = client.messages.list(limit=2)
for m in some_messages:
    messageId = m.sid
    if (messageId[:1] == "M"):
        message = client.messages(messageId).fetch()
        print(message.sid)
media = client.messages(message.sid).media.list()
for record in media:
    print(record.uri)
    img = (TWILIO_BASE_URI + str(record.uri)).strip(".json'").strip("u'")

try:
    response = requests.get(img, stream=True).raw
except requests.exceptions.RequestException as e:  
    sys.exit(1)

try:
    img = Image.open(response)
    imgW = float(img.size[0])
    imgH = float(img.size[1])
    print(imgW)
    print(imgH)
    imgRatio = imgW/imgH
    print(imgRatio)
    if (imgRatio >= INKY_RATIO):
        img = img.resize((int(INKY_WIDTH), int((1/imgRatio)*INKY_WIDTH)), resample=Image.BILINEAR) 
        img = img.crop((0, 0, int(INKY_WIDTH), int(INKY_HEIGHT)))
    else:
        img = img.resize((int(imgRatio*INKY_HEIGHT), int(INKY_HEIGHT)), resample=Image.BILINEAR)
        img = img.crop(((int((img.size[0]-INKY_WIDTH)/2), 0, int((img.size[0]-INKY_WIDTH)/2)+int(INKY_WIDTH), int(INKY_HEIGHT))))
    img = ImageOps.posterize(img, bits=1)
    recolor(img)
    img.show()
except IOError:
    print("Unable to open image")
    sys.exit(1)

