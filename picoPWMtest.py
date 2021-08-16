import machine
import utime

print("starting")

led_pin = machine.Pin(25, machine.Pin.OUT)
pin_out = machine.Pin(6, machine.Pin.OUT)
pwm_pin_in = machine.Pin(28, machine.Pin.IN)
# pwm_pin_in = machine.Pin(28)

# while True:
#     led_pin.value(1)
#     utime.sleep(1)
#     led_pin.value(0)
#     utime.sleep(1)

pin_out.value(1)
utime.sleep(.1)
print(pwm_pin_in.value())
# print(machine.ADC(2).read_u16())
utime.sleep(.1)

pin_out.value(0)
utime.sleep(.1)
print(pwm_pin_in.value())
# print(machine.ADC(2).read_u16())




i = 0
prev_vol = 0
prev_pos = "down"
high_count = 0
high = 1
low = 0
threshold = 20
while True:
    curr_vol = pwm_pin_in.value()
    if curr_vol == high and prev_vol == high:
        high_count+=1
    elif curr_vol == low and prev_vol == high:
        curr_pos = "up" if high_count > threshold else "down"
        high_count = 0

        if curr_pos != prev_pos:
    #       print(curr_pos)
            print("=================")
            prev_pos = curr_pos
            
#         print(curr_pos)


    prev_vol = curr_vol
        
        
        
        
#     value = int(i/100)%2
#     pin_out.value(value)
#     print(value)
#     print(curr)
#     print(machine.ADC(pwm_pin_in).read_u16())

    
#     utime.sleep(.01)
    i+=1
