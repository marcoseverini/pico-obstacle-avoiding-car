from machine import Pin  # Import the Pin module to interact with GPIO pins
import time  # Import the time module for timing functions

# Function to measure distance using the ultrasonic sensor
def distance(TRIG, ECHO):
    TRIG.low()  # Set TRIG to low to ensure a clean pulse
    time.sleep_us(2)  # Short delay to stabilize the sensor
    TRIG.high()  # Set TRIG to high to start the ultrasonic pulse
    time.sleep_us(10)  # Wait 10 microseconds for the pulse
    TRIG.low()  # Set TRIG to low to end the pulse

    # Wait for the ECHO pin to go high (start receiving the echo)
    while not ECHO.value():
        pass

    time1 = time.ticks_us()  # Record the time when the pulse is sent

    # Wait for the ECHO pin to go low (end of the echo reception)
    while ECHO.value():
        pass

    time2 = time.ticks_us()  # Record the time when the pulse is received

    # Calculate the time difference between sending and receiving the pulse
    duration = time.ticks_diff(time2, time1)

    # Calculate distance in centimeters (speed of sound = 340 m/s)
    return duration * 340 / 2 / 10000  

# Pin assignments for motor control (left and right motors)
inSx1 = Pin(13, Pin.OUT)  # Left motor control pin 1
inSx2 = Pin(12, Pin.OUT)  # Left motor control pin 2
inDx1 = Pin(11, Pin.OUT)  # Right motor control pin 1
inDx2 = Pin(10, Pin.OUT)  # Right motor control pin 2

# Pin assignments for ultrasonic sensors (left and right)
TRIG_sx = Pin(19, Pin.OUT)  # Trigger pin for the left sensor
ECHO_sx = Pin(18, Pin.IN)   # Echo pin for the left sensor
TRIG_dx = Pin(3, Pin.OUT)   # Trigger pin for the right sensor
ECHO_dx = Pin(2, Pin.IN)    # Echo pin for the right sensor

# Function to move the robot forward
def forward():
    inSx1.value(0)  # Set left motor to forward
    inSx2.value(1)
    inDx1.value(0)  # Set right motor to forward
    inDx2.value(1)

# Function to stop the robot
def stop():
    inSx1.value(0)  # Set both motors to stop
    inSx2.value(0)
    inDx1.value(0)
    inDx2.value(0)

# Function to move the robot backward
def backward():
    inSx1.value(1)  # Set left motor to backward
    inSx2.value(0)
    inDx1.value(1)  # Set right motor to backward
    inDx2.value(0)

# Function to turn the robot slightly to the right while moving forward
def forward_dx():
    inSx1.value(0)  # Left motor forward
    inSx2.value(1)
    inDx1.value(1)  # Right motor backward (for turning)
    inDx2.value(0)

# Function to turn the robot slightly to the left while moving forward
def forward_sx():
    inSx1.value(1)  # Left motor backward (for turning)
    inSx2.value(0)
    inDx1.value(0)  # Right motor forward
    inDx2.value(1)

# Initial delay for system setup
time.sleep(5)

# Main loop to control the robot's movement
while True:
    forward()  # Start moving forward
    time.sleep_ms(100)  # Wait for 100 milliseconds

    # Measure distance from the left and right sensors
    dis_sx = distance(TRIG_sx, ECHO_sx)
    time.sleep_ms(100)  # Short delay between readings
    dis_dx = distance(TRIG_dx, ECHO_dx) 

    # Print the measured distances
    print("Distance SX: %.2f cm" % dis_sx)
    print("Distance DX: %.2f cm" % dis_dx)

    # Check if an obstacle is detected within 10 cm by either sensor
    if dis_sx < 10 or dis_dx < 10:
        stop()  # Stop the robot
        time.sleep(1)  # Wait for a second
        backward()  # Move backward to avoid the obstacle
        time.sleep_ms(500)  # Continue backward for 500 milliseconds

        # Decide which direction to turn based on sensor readings
        if dis_dx > dis_sx:  # Turn right if there is more space on the right
            forward_dx()
            time.sleep_ms(500)  # Continue turning for 500 milliseconds
        else:  # Turn left if there is more space on the left
            forward_sx()
            time.sleep_ms(500)  # Continue turning for 500 milliseconds
