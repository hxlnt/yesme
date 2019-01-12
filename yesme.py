from dotenv import load_dotenv
import os
from PIL import Image, ImageEnhance
import requests
import sys
from twilio.rest import Client

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)
TWILIO_BASE_URI = "https://api.twilio.com"

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
    img.show()
except IOError:
    print("Unable to open image")
    sys.exit(1)