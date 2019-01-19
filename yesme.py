from dotenv import load_dotenv
from inky import InkyPHAT
import os
from PIL import Image, ImageOps
import requests
import threading
from twilio.rest import Client

load_dotenv(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env'))
latestImgUrl = ""

# Getting latest media-containing message from Twilio
def getLatestMediaMsg(msgarray):
    for msg in msgarray:
        if msg.sid[:1] == "M":
            latestMsg = client.messages(msg.sid).fetch()
            return latestMsg
    return None

# Downsample method
def recolor(img):
    inky_img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
    for y in range(inky_display.HEIGHT):
        for x in range(inky_display.WIDTH):
            pixelMap = img.load()
            if (pixelMap[x,y] == (128,128,128) or pixelMap[x,y] == (255,255,255)):
                inky_img.putpixel((x,y), inky_display.WHITE)
            elif pixelMap[x,y] == (0, 0, 0):
                inky_img.putpixel((x,y), inky_display.BLACK)
            else:
                inky_img.putpixel((x,y), inky_display.YELLOW)
    return inky_img

def main():
    threading.Timer(120, main).start()
    global latestImgUrl
    try:
        incomingMsgs = client.messages.list(to=os.getenv('TWILIO_PHONE_NUMBER'))
        sortedMsgList = sorted(incomingMsgs, key=lambda msg:msg.date_sent, reverse=True)
        latestMediaMsg = getLatestMediaMsg(sortedMsgList)
        latestImg = client.messages(latestMediaMsg.sid).media.list(limit=1)[0]
        if (latestImgUrl != ("https://api.twilio.com" + str(latestImg.uri)).strip(".json'").strip("u'")):
            latestImgUrl = ("https://api.twilio.com" + str(latestImg.uri)).strip(".json'").strip("u'")
            img = requests.get(latestImgUrl, stream=True).raw
            # Resize and crop incoming image
            img = Image.open(img)
            img = img.rotate(90, expand=1)
            imgW = float(img.size[0])
            imgH = float(img.size[1])
            imgRatio = imgW/imgH
            if (imgRatio < float(inky_display.WIDTH)/float(inky_display.HEIGHT)):
                img = img.resize((inky_display.WIDTH, int(inky_display.WIDTH/imgRatio)), resample=Image.BILINEAR)
                imgHeightMargin = int((img.size[1]-inky_display.HEIGHT)/2)
                img = img.crop((0, imgHeightMargin, inky_display.WIDTH, inky_display.HEIGHT+imgHeightMargin))        
            else:
                img = img.resize((int(imgRatio*inky_display.HEIGHT), inky_display.HEIGHT), resample=Image.BILINEAR)
                imgWidthMargin = int((img.size[0]-inky_display.WIDTH)/2)
                img = img.crop((imgWidthMargin, 0, inky_display.WIDTH+imgWidthMargin, inky_display.HEIGHT))
            img = img.convert(mode="P", dither=1, palette="ADAPTIVE", colors=256)
            img = img.convert(mode="RGB")
            img = ImageOps.posterize(img, bits=1)
            img = recolor(img)
            inky_display.set_image(img)
            inky_display.show()

    except requests.exceptions.RequestException as e:
        print("Could not grab latest image:")
        print(e)
        sys.exit(1)

# Initialize Twilio client
client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))

# Initialize inky display
inky_display = InkyPHAT("yellow")

main()
