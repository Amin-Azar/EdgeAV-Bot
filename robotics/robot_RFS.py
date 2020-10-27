import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

class Motor():
    direction_pins = None
    enable_pin = None
    enable_is_pwm = False
    pwm = None
    speed = 0
    def __init__(self, direction_pins, enable_pin=None, enable_is_pwm=False):
        # Direction
        self.direction_pins = direction_pins # [35,36]
        GPIO.setup(self.direction_pins[0],GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.direction_pins[1],GPIO.OUT,initial=GPIO.LOW)
        # PWM (if any)
        self.enable_is_pwm = enable_is_pwm
        if self.enable_is_pwm:
            if enable_pin not in [32,33]:
                raise "Jetson's pwm pins are #32 and #33 !!"
            self.enable_pin = enable_pin # 32
            GPIO.setup(enable_pin,GPIO.OUT)
            self.pwm=GPIO.PWM(enable_pin,50)
            self.pwm.start(0)
        else:
            # ON/OFF motor
            if enable_pin:
                self.enable_pin = enable_pin
                GPIO.setup(self.enable_pin,GPIO.OUT,initial=GPIO.LOW)
            #else: assume an always ENABLE driver channel.
        # initiaize motors to stop
        self.release()

    def set_pins(self, pin0=GPIO.LOW, pin1=GPIO.LOW):
        GPIO.output(self.direction_pins[0],pin0)
        GPIO.output(self.direction_pins[1],pin1)
    def set_speed(self, speed=0):
        self.speed = ((speed - (-1))/2)*100
        if self.enable_is_pwm:
            self.pwm.ChangeDutyCycle(self.speed)
        else:
            if self.enable_pin:
                if speed == 0:
                    GPIO.output(self.enable_pin,GPIO.LOW) # OFF
                else:
                    GPIO.output(self.enable_pin,GPIO.HIGH) # ON
    def CW(self, speed=1):
        self.set_pins(GPIO.HIGH, GPIO.LOW)
        self.set_speed(speed)
    def CCW(self, speed=1):
        self.set_pins(GPIO.LOW, GPIO.HIGH)
        self.set_speed(speed)
    def stop(self, speed=0):
        self.set_pins(GPIO.LOW, GPIO.LOW)
        self.set_speed(speed)
    def release(self, speed=-1):
        self.set_pins(GPIO.LOW, GPIO.LOW)
        self.set_speed(speed)


class Robot():
    """
        Motors: rear_motor | front_motor | steer_motor
    """
    def __init__(self, *args, **kwargs):
        super(Robot, self).__init__(*args, **kwargs)
        # initialize motors and pins
        self.rear_motor  = Motor([29,31], 32, enable_is_pwm=True)
        self.front_motor = Motor([35,36], 33, enable_is_pwm=True)
        self.steer_motor = Motor([37,38]) #40
        self.release_all()
    def forward(self, speed=1.0):
        # release steer
        self.rear_motor.CW(speed)
        self.rear_motor.CW(speed)
        self.steer_motor.release()
    def forward_l(self, speed=1.0):
        self.rear_motor.CW(speed)
        self.rear_motor.CW(speed)
        self.steer_motor.CW()
    def forward_r(self, speed=1.0):
        self.rear_motor.CW(speed)
        self.rear_motor.CW(speed)
        self.steer_motor.CCW()
    def backward(self, speed=1.0):
        # release steer
        self.rear_motor.CCW(speed)
        self.rear_motor.CCW(speed)
        self.steer_motor.release()
    def backward_l(self, speed=1.0):
        self.rear_motor.CCW(speed)
        self.rear_motor.CCW(speed)
        self.steer_motor.CW()
    def backward_r(self, speed=1.0):
        self.rear_motor.CCW(speed)
        self.rear_motor.CCW(speed)
        self.steer_motor.CCW()
    def stop(self):
        # LOCK rear & front
        self.rear_motor.stop()
        self.front_motor.stop()
        self.steer_motor.release()
    def release(self):
        # enable = 0
        self.rear_motor.release()
        self.front_motor.release()
        self.steer_motor.release()