from vex import *
from robot_config import * 

# manual control
def user_control():
    
    # automatically at brake for accuracy
    Drivetrain.set_stopping(Brake)
    
    ConveyorBelt.set_stopping(Hold)
    Intake.set_stopping(Hold)
    
    mech_speed = 90
    # consistent speed
    
    while True:
        
        
    # arcade drive, NOT tank drive right now
      #  Axis 3 (left joystick vertical) for Forward/Reverse speed (Throttle)
        throttle = Controller1.axis3.position()
        
        # Axis 1 (left joystick horizontal) for Left/Right turn (Steering)
        steering = Controller1.axis1.position()
        
        left_power = throttle + steering
        right_power = throttle - steering
                LeftMotor.spin(FORWARD, left_power, PercentUnits.PCT)
        RightMotor.spin(FORWARD, right_power, PercentUnits.PCT)
        
        
        # Press R1
        if Controller1.buttonR1.pressing():
            Intake.spin(FORWARD, mech_speed, PercentUnits.PCT)
            ConveyorBelt.spin(FORWARD, mech_speed, PercentUnits.PCT)
        
        # Press R2
        elif Controller1.buttonR2.pressing():
            Intake.spin(REVERSE, mech_speed, PercentUnits.PCT)
            ConveyorBelt.spin(REVERSE, mech_speed, PercentUnits.PCT)
            
        else:
            Intake.stop()
            ConveyorBelt.stop()

        
        brain.screen.set_cursor(1, 1)
        if BumperSwitch.pressing():
            brain.screen.print("BUMBER PRESSED ")
        else:
            brain.screen.print("BUMPER OPEN  ")

        # 15 millisecond wait time right now, subject to change
        wait(15, MSEC)


Competition = Competition()
Competition.drivercontrol(user_control)
# when driver timer starts, code goes into effect.
