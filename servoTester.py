from pyaxidraw import axidraw   # import module
import math
import time

ad = axidraw.AxiDraw()          # Initialize class
ad.interactive()                # Enter interactive context
ad.connect()                    # Open serial port to AxiDraw


ad.options.units = 2
ad.options.speed_penup = 100
ad.options.pen_rate_raise = 100
ad.options.pen_rate_lower = 100
ad.options.pen_pos_up = 100
ad.options.pen_pos_down = 0
ad.update()                 # Process changes to options



while True:
    ad.pendown()
    print("down")
    time.sleep(1.5)
    ad.penup()
    print("up")
    time.sleep(1.5)

