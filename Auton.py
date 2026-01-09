#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()


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

# Library imports
from vex import *
# ------------------------------------------
# Project: V5 Push Back - Center Field Auton
# Strategy: Drive to center, intake balls, push to goal
# ------------------------------------------

# --- Hardware Configuration (Aligned with totalmain1) ---
brain = Brain()
LeftMotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
RightMotor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
Drivetrain = DriveTrain(LeftMotor, RightMotor, 12.56, 12.5, DistanceUnits.IN)

ConveyorBelt = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
IntakeMain = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)
IntakePortD = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)

# Sensors
inertial_sensor = Inertial(Ports.PORT8)
# Distance sensor (assuming Port 9 based on your requirement)
dist_sensor = Distance(Ports.PORT9) 

# --- Helper Functions ---

def run_intake(speed_pct=100):
    IntakeMain.spin(FORWARD, speed_pct, PERCENT)
    IntakePortD.spin(FORWARD, speed_pct, PERCENT)
    ConveyorBelt.spin(FORWARD, speed_pct, PERCENT)

def stop_intake():
    IntakeMain.stop(BrakeType.HOLD)
    IntakePortD.stop(BrakeType.HOLD)
    ConveyorBelt.stop(BrakeType.HOLD)

def score_reverse(duration_ms=1500):
    IntakeMain.spin(REVERSE, 100, PERCENT)
    IntakePortD.spin(REVERSE, 100, PERCENT)
    ConveyorBelt.spin(REVERSE, 100, PERCENT)
    wait(duration_ms, MSEC)
    stop_intake()

# --- Autonomous Routine ---

def autonomous():
    # 1. Sensor Calibration
    inertial_sensor.calibrate()
    while inertial_sensor.is_calibrating():
        wait(25, MSEC)
    
    # 2. Setup
    Drivetrain.set_drive_velocity(70, PERCENT)
    Drivetrain.set_turn_velocity(50, PERCENT)
    
    # 3. Drive to Center (Adjust 24-30 inches based on starting position)
    # Start intake early to catch balls in the middle
    run_intake(100)
    Drivetrain.drive_for(FORWARD, 28, INCHES)
    
    # 4. Use Distance Sensor to find or avoid the center barrier/balls
    if dist_sensor.object_distance(INCHES) < 4:
        # Small adjustment if too close to an object
        Drivetrain.drive_for(REVERSE, 2, INCHES)
    
    # 5. Sweep for more balls
    Drivetrain.turn_for(RIGHT, 30, DEGREES)
    Drivetrain.drive_for(FORWARD, 10, INCHES)
    Drivetrain.turn_for(LEFT, 60, DEGREES)
    
    # 6. Drive toward the scoring zone (Goal)
    # Adjust heading back toward your target goal
    Drivetrain.turn_for(RIGHT, 30, DEGREES) 
    Drivetrain.drive_for(FORWARD, 15, INCHES)
    
    # 7. Release/Push balls into scoring area
    score_reverse(2000)
    
    # 8. Reset to clear the area
    Drivetrain.drive_for(REVERSE, 10, INCHES)
    stop_intake()

# --- Competition Setup ---
# user_control logic from totalmain1 remains the same
def user_control():
    Drivetrain.set_stopping(BrakeType.BRAKE)
    while True:
        throttle = Controller1.axis3.position()
        steering = Controller1.axis1.position()
        LeftMotor.spin(FORWARD, throttle + steering, PERCENT)
        RightMotor.spin(FORWARD, throttle - steering, PERCENT)
        # ... (Rest of your controller logic)
        wait(20, MSEC)

competition = Competition(user_control, autonomous)
