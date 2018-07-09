# Steganography
Program that puts given message onto pixels of given image. Number of bits can be set for each color.

## Used libraries
* opencv-python - reading bits of image,
* bitarray - bit conversions.

Can be installed with ```pip install -r requirements.txt```.

## Input
* example.jpg - file placed inside the same folder, can be changed in 71st line,
* red, green, blue - how many bits of each color to allocate,
* msg - message to be placed on the image.

## Output
* steginput.png - input image copy,
* stegoutput.png - output image.

## Warnings
Do not change the PNG format to JPG output as compression ruins the message.
