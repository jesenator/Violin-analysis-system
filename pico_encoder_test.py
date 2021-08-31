from machine import Pin, PWM
import utime





hammer_pin1 = Pin(7, Pin.OUT)
hammer_pin2 = Pin(8, Pin.OUT)
hammer_pin3 = Pin(9, Pin.OUT)
encoderA = Pin(14, Pin.IN)
encoderB = Pin(15, Pin.IN)


pwm = PWM(hammer_pin3)
pwm.freq(50)
pwm.duty_ns(0)

hammer_pin1.high()
hammer_pin2.low()

pwm.duty_ns(4000000)

high = 1
low = 0
prevA = encoderA.value()
encoder_count = 1

total_count = 1920 / 2
while encoder_count % total_count != 0:
    currA = encoderA.value()
#     print(currA)
    if currA == low and prevA == high:
        encoder_count+=1
        print(encoder_count)

    prevA = currA
pwm.duty_ns(0)
