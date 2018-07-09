import cv2, bitarray

# break out of nested loop by raising:
class NestedLoopsBreaker(Exception): pass

# ----------new----------
# message to bitstring
# stackoverflow q: 10237926, u: 455506
def stringtobitstring(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result


# img[x][y][channel] to bitarray
def inttobitarray(intval):
    return bitarray.bitarray(format(intval, '08b'))

def bitarraytoint(bitarr):
    result = 0
    for bit in range(len(bitarr)):
        result = (result << 1) | bitarr[bit]
    return result
# -------end new----------

# information
print('''String is at first converted to 8-bit ASCII, then copied into picture from string's MSB to pixel's MSB. L/MSB = Least/Most Significant Bit''')

# user input
red = 9
green = 9
blue = 9

while int(red) > 8 or int(red) < 0:
    red = input('How many red bits would you like to allocate [0-8]\n')
while int(green) > 8 or int(green) < 0:
    green = input('How many green bits would you like to allocate [0-8]\n')
while int(blue) > 8 or int(blue) < 0:
    blue = input('How many blue bits would you like to allocate [0-8]\n')

msg = input('\n\nInput message:\n')

# msg len
msgbitlen = len(msg)*8

# number strings to int and message to bytes (via int) conversion for user input numbers
r = int(red)
g = int(green)
b = int(blue)

# swapping bit in bitarray
msgbitstring = stringtobitstring(msg)
print(msgbitstring)
msgpos = 0

# image read (and its characteristics)
img = cv2.imread("example.jpg")
height, width, channels = img.shape

# max bit len on pic with given values per channel
currentMaxMsgLength = width*height*(r+g+b)
print(str(width) + 'x' + str(height) + '*(r' + str(red) + '+g' + str(green) + '+b' + str(blue) + ') = ' + str(currentMaxMsgLength))

if currentMaxMsgLength < msgbitlen:
    print('err: given message is too long for that picture!')
    exit(0)

cv2.imwrite("steginput.png", img)

# beg = 0
# end = 7

imgXYCbitarray = bitarray.bitarray()

try:
    for x in range(width):
        for y in range(height):

            # blue channel
            imgXYCbitarray = inttobitarray(img[x][y][0])  # saving img[x][y][c] bitarray to variable
            for intpos in range(8 - b, 8):
                if msgpos < msgbitlen:
                    imgXYCbitarray[intpos] = msgbitstring[msgpos]  # swapping bits
                    msgpos += 1  # msgpos refreshing
                else:
                    raise NestedLoopsBreaker

            img[x][y][0] = bitarraytoint(imgXYCbitarray)  # saving new value onto picture

            # green channel
            imgXYCbitarray = inttobitarray(img[x][y][1])  # saving img[x][y][c] bitarray to variable
            for intpos in range(8 - g, 8):
                if msgpos < msgbitlen:
                    imgXYCbitarray[intpos] = msgbitstring[msgpos]  # swapping bits
                    msgpos += 1  # msgpos refreshing
                else:
                    raise NestedLoopsBreaker

            img[x][y][1] = bitarraytoint(imgXYCbitarray)  # saving new value onto picture

            # red channel
            imgXYCbitarray = inttobitarray(img[x][y][2])  # saving img[x][y][c] bitarray to variable
            for intpos in range(8 - r, 8):
                if msgpos < msgbitlen:
                    imgXYCbitarray[intpos] = msgbitstring[msgpos]  # swapping bits
                    msgpos += 1  # msgpos refreshing
                else:
                    raise NestedLoopsBreaker

            img[x][y][2] = bitarraytoint(imgXYCbitarray)  # saving new value onto picture

except NestedLoopsBreaker:
    pass


cv2.imwrite("stegoutput.png", img)