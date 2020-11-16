# EdgeAV-Bot

# Initialization

Jetson has 2 PWM pins (pin 32,33).
Need to enable them running the following script once:

```
bash enable_pwm.sh
```

# Robot Movements

Driver choice:
 - 2x L298N Dual H Bridge Motor Controller Board [link](https://www.amazon.ca/gp/product/B0786L5YPP/ref=ppx_yo_dt_b_asin_title_o05_s00?ie=UTF8&psc=1). Each can drve 2 motors and as we are using 3 motors, we need 2 of these modules. (Although we could connect the back and front motors to the same channel, we decided to keep them separate for more flexibility).
<img src="https://images-na.ssl-images-amazon.com/images/I/61OiJgvqwsL._AC_SL1001_.jpg" alt="Drivers" width="300"/>

Motors:
 - Motor1: Rear axle - brushed DC motor. [PWM controlled - pin 32]
 - Motor2: Front axle - brushed DC motor. [PWM controlled - pin 33]
 - Motor3: Steering - brushed DC motor. [ON/OFF =(L/R)]

<img src="../resources/bot-buttom.jpg" alt="Motors" width="300"/>
<img src="../resources/bot-pin.jpg" alt="Pins" width="300"/>


# Note

The JetBot from Nvidia, is a differential drive robot which uses 2 Left and Right motors (no Steering Motor) !
