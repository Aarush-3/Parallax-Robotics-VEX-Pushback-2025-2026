from vex import *

brain = Brain()
# create brain

# --- Drivetrain Motors ---
# This is for Port 1: Left side motor (False = not reversed)
LeftMotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
# This is for Port 2: Right side motor (True = MUST be reversed for the robot to drive straight)
RightMotor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)


Drivetrain = DriveTrain(LeftMotor, RightMotor, 12.56, 12.5, DistanceUnits.INCHES)

ConveyorBelt = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
Intake = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)

Controller1 = Controller(Primary.CONTROLLER)
BumperSwitch = Bumper(Ports.PORTD)


