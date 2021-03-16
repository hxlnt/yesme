
# Y.E.S.




| 
![Y.E.S. you can!](yesme.gif) | Y.E.S. is the **Y**ellow **e**Ink **S**elfie Photo Booth.<BR><BR>It's a Raspberry Pi outfitted with a [Pimoroni eInk display](https://shop.pimoroni.com/products/inky-phat?variant=12549254905939) and housed in a cute photo booth! Text a photo to the Y.E.S., and it will magically appear on the dazzling three color eInk screen. |
| ------ | :------ |
|        |         |



## How to build it
1. Set yourself up with a Twilio account and number.
2. Clone this repo down to a Raspberry Pi outfitted with Pimoroni's Inky pHat.
3. Fill in the variables in ``.env`` with your Twilio shtuff.
4. After installing dependencies (``pip install -r requirements.txt``), run the Python script: ``python yesme.py``. Better yet, have the script run automatically run on boot. (Google "crontab -e @reboot python" if you wanna know how to get that set up.)
5. Text a selfie to your Twilio number. The script will take care of resizing and downsampling.
6. Give the number out to trusted friends. (I cannot stress the "trusted" part enough, y'all. Don't let randos up in here.) Y.E.S. will display the most recent image. It checks every two minutes for new images. It ignores text messages.

You can, of course, continue using the Y.E.S. as a regular Raspberry Pi. It'll just run this in the background. And because the display is eInk, images will be retained if the Raspberry Pi is powered down.

## Testing
I didn't write proper unit tests, but you can test this out without the Pi by running ``python yesme-test.py``. This will remove the Inky pHat dependency and show you the image on your operating system's default image preview application.

## Add more features (D.I.Y.)
Here are some features I thought about adding:
 - Add text message support via the inky API
 - Add image cycling to the Python script
 - Switch between "recent image" mode and "image cycling" mode via a text-message control code from your personal number
 
Maybe I'll get around to 'em some day. Or, hey, I'll take your PRs.

## The housing
It's made from stained/painted basswood with a little holographic vinyl, all cut with the Cricut Explore Air. The curtain is made from lamé and serves the purpose of disguising the USB power cable as a curtain rod.
