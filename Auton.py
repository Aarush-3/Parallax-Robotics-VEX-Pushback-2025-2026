#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
left_motor_a = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain_inertial = Inertial(Ports.PORT5)
drivetrain = SmartDrive(left_drive_smart, right_drive_smart, drivetrain_inertial, 319.19, 320, 40, MM, 1)
distance_6 = Distance(Ports.PORT6)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()

vexcode_initial_drivetrain_calibration_completed = False
def calibrate_drivetrain():
    # Calibrate the Drivetrain Inertial
    global vexcode_initial_drivetrain_calibration_completed
    sleep(200, MSEC)
    brain.screen.print("Calibrating")
    brain.screen.next_row()
    brain.screen.print("Inertial")
    drivetrain_inertial.calibrate()
    while drivetrain_inertial.is_calibrating():
        sleep(25, MSEC)
    vexcode_initial_drivetrain_calibration_completed = True
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)


# Calibrate the Drivetrain
calibrate_drivetrain()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode V5 Python Project
# 
# ------------------------------------------

# Begin project code

ConveyorBelt = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
IntakeMain = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)

drivetrain.set_drive_velocity(50, PERCENT)
drivetrain.set_turn_velocity(60, PERCENT)
IntakeMain.set_velocity(100, PERCENT)
ConveyorBelt.set_velocity(80, PERCENT)

def autonomous():
    drivetrain.turn_to_heading(270, DEGREES)
    drivetrain.drive(FORWARD)

    while distance_6.object_distance(MM) > 120 and brain.timer.time(SECONDS) < 3:
        wait (10, MSEC)

    drivetrain.stop()

    drivetrain.turn_for(LEFT, 90, DEGREES)

    IntakeMain.spin(FORWARD)
    wait(2, SECONDS)

    drivetrain.turn_for(RIGHT, 135, DEGREES)

    drivetrain.drive(FORWARD)
    while distance_6.object_distance(MM) > 150 and brain.timer.time(SECONDS) < 3:
        wait(10, MSEC)
    drivetrain.stop()

    ConveyorBelt.spin(FORWARD)
    wait(2,SECONDS)

    IntakeMain.stop()
    ConveyorBelt.stop()

    drivetrain.drive_for(REVERSE, 300, MM)
