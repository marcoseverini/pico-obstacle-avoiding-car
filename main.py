from machine import Pin
import time

def distance(TRIG, ECHO):
    TRIG.low()  
    time.sleep_us(2) 
    TRIG.high() 
    time.sleep_us(10) 
    TRIG.low()  

    while not ECHO.value():
        pass

    time1 = time.ticks_us() 

    while ECHO.value():
        pass

    time2 = time.ticks_us()  

    during = time.ticks_diff(time2, time1)

    return during * 340 / 2 / 10000  

# Configura i pin dei motori
inSx1 = Pin(13, Pin.OUT)
inSx2 = Pin(12, Pin.OUT)
inDx1 = Pin(11, Pin.OUT)
inDx2 = Pin(10, Pin.OUT)

# Configura i pin dei sensori
TRIG_sx = Pin(19, Pin.OUT)
ECHO_sx = Pin(18, Pin.IN)
TRIG_dx = Pin(3, Pin.OUT)
ECHO_dx = Pin(2, Pin.IN)

def forward():
    inSx1.value(0)
    inSx2.value(1)
    inDx1.value(0)
    inDx2.value(1)

def stop():
    inSx1.value(0)
    inSx2.value(0)
    inDx1.value(0)
    inDx2.value(0)

def backward():
    inSx1.value(1)
    inSx2.value(0)
    inDx1.value(1)
    inDx2.value(0)

def forward_dx():
    inSx1.value(0)
    inSx2.value(1)
    inDx1.value(1)
    inDx2.value(0)

def forward_sx():
    inSx1.value(1)
    inSx2.value(0)
    inDx1.value(0)
    inDx2.value(1)

# Pausa di inizializzazione
time.sleep(5)

while True:
    forward()
    time.sleep_ms(100)
    dis_sx = distance(TRIG_sx, ECHO_sx)
    time.sleep_ms(100)
    dis_dx = distance(TRIG_dx, ECHO_dx) 

    print("Distance SX: %.2f cm" % dis_sx)
    print("Distance DX: %.2f cm" % dis_dx)

    if dis_sx < 10 or dis_dx < 10:
        stop()
        time.sleep(1)
        backward()
        time.sleep_ms(500)
        if dis_dx > dis_sx:
            forward_dx()
            time.sleep_ms(500)
        else:
            forward_sx()
            time.sleep_ms(500)

