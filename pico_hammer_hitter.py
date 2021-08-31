from machine import Pin, PWM
from utime import sleep, ticks_ms, ticks_diff

def get_seconds(start_ms):
#     print(start_ms)
    seconds = round(ticks_diff(ticks_ms(), start_ms)/1000 * 1000) /1000
    return seconds


def hit_hammer(encoder_count):
    print("================================")
    start_ms = ticks_ms()
    pwm.duty_ns(8000000)
    prevA = encoderA.value()
#     total_count = 1920 / 2 * 5
    total_count = 4750 / 5 * 5

    done = False
    extra_seconds = 1
    while True:
        if get_seconds(start_ms) % 1 == 0:
            print(get_seconds(start_ms))
        currA = encoderA.value()
        if currA == low and prevA == high:
            encoder_count+=1
#             if encoder_count % 10 == 0:
#                 print(encoder_count)

        prevA = currA
        
        if encoder_count % total_count == 0 and not done:
            done = True
            pwm.duty_ns(0)
            print("CHANGING+++++++++++++++++")
            print("time = 0")
            start_ms = ticks_ms()
            
        if done and get_seconds(start_ms) > extra_seconds:
            return encoder_count



print("starting")
hammer_pin1 = Pin(7, Pin.OUT)
hammer_pin2 = Pin(8, Pin.OUT)
hammer_pin3 = Pin(9, Pin.OUT)
encoderA = Pin(14, Pin.IN)
encoderB = Pin(15, Pin.IN)

pwm = PWM(hammer_pin3)
pwm.freq(50)
pwm.duty_ns(0)
encoder_count = 1

hammer_pin1.high()
hammer_pin2.low()


# pin_out = Pin(6, Pin.OUT)
pwm_pin_in = Pin(27, Pin.IN)
led_pin = Pin(28, Pin.IN)


i = 0
prev_vol = 0
prev_pos = "down"
high_count = 0
high = 1
low = 0
threshold = 20
while True:
#     print("going#)
    curr_vol = pwm_pin_in.value()
    if curr_vol == high and prev_vol == high:
        high_count+=1
    elif curr_vol == low and prev_vol == high:
        curr_pos = "up" if high_count > threshold else "down"

        high_count = 0

        if curr_pos != prev_pos:
            print(curr_pos)
            prev_pos = curr_pos
            if curr_pos == "down":
                encoder_count = hit_hammer(encoder_count)
                pass
#         print(curr_pos)


    prev_vol = curr_vol
        




