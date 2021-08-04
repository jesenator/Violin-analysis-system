import time

from pyaxidraw import axidraw   # import module
import math
import time


def getXY(radius, angle):
    x = round(radius * -math.cos(angle))
    y = round(radius * -math.sin(angle))
    return x, y


def getCoordinates(angles, radii):
    xCoords = []
    yCoords = []
    for angle in angles:
        for radius in radii:
            angle = (angle + 90) / 360 * 2 * math.pi
            x, y = getXY(radius, angle)
            xCoords.append(x)
            yCoords.append(y)
            # print(str(radius) + ", " + str(angle))
            # print(str(x) + ", " + str(y))
            ad.moveto(x, y)
    return xCoords, yCoords


centerX = 150
centerY = 109
# centerY = 90
maxRadi = min(centerX, centerY)
angleNum = 16
radiusNum = 4
totalPostions = angleNum * radiusNum
print("total positions: " + totalPostions)
hits = 1
angles = []
radii = []
xCoords = []
yCoords = []

ad = axidraw.AxiDraw()          # Initialize class
ad.interactive()                # Enter interactive context
ad.connect()                    # Open serial port to AxiDraw

ad.options.units = 2
ad.options.speed_penup = 100
ad.options.pen_rate_raise = 100
ad.options.pen_rate_lower = 100
ad.update()                 # Process changes to options
ad.moveto(centerX, centerY)
print("center hammer on the plate")
time.sleep(2)

for i in range(angleNum):
    angle = 360 * i / angleNum + 90
    angle = angle / 360 * 2 * math.pi
    angles.append(angle)
for i in range(radiusNum):
    radii.append(round(maxRadi * (i+1) / radiusNum, 2))
print(angles)
print(radii)
# xCoords, yCoords = getCoordinates(angles, radii)

for angle in angles:
    for radius in radii:
        x, y = getXY(radius, angle)
        x += centerX
        y += centerY
        # print("polar: " + str(radius) + ", " + str(angle/math.pi) + "pi")
        # print("cartesian: " + str(x) + ", " + str(y))

        ad.moveto(x, y)
        xCoords.append(x)
        yCoords.append(y)

        for i in range(hits):
            ad.pendown()
            ad.penup()
            # time.sleep(.2)
        # time.sleep(.5)

    # ad.moveto(centerX, centerY)
    # time.sleep(.5)

ad.moveto(0, 0)
# paste coords lists to main program
print(xCoords)
print(yCoords)
ad.disconnect()                 # Close serial port to AxiDraw
