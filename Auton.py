# ------------------------------------------
# Project:      VEXcode Project - Fixed Autonomous
# Description:  VEXcode V5 Python Project
# ------------------------------------------
from vex import *

brain = Brain()

# --- Drivetrain Motors ---
LeftMotor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
RightMotor = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)

# FIX 1: Changed 'INCHES' to 'DistanceUnits.IN'
Drivetrain = DriveTrain(LeftMotor, RightMotor, 12.56, 12.5, DistanceUnits.IN)

# Intake/Conveyor System
ConveyorBelt = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
Intake = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)

# Sensors
inertial_sensor = Inertial(Ports.PORT8)
vision_sensor = Vision(Ports.PORT5)

# --- Vision Signature Setup ---
BLOCK_SIG = Signature(1, 5, 500, 75, 500, 90, 500, 1.5, 0)
GOAL_SIG = Signature(2, 40, 500, 85, 500, 95, 500, 1.5, 0)

# --- Movement and Action Functions ---

def set_drive_speed(speed=60):
    Drivetrain.set_drive_velocity(speed, PERCENT)
    Drivetrain.set_turn_velocity(speed * 0.7, PERCENT)

def turn_to_angle(angle_degrees, speed=40):
    Drivetrain.set_turn_velocity(speed, PERCENT)
    # FIX 2: Corrected direction constants to RIGHT/LEFT
    if angle_degrees >= 0:
        Drivetrain.turn_for(RIGHT, angle_degrees, DEGREES)
    else:
        Drivetrain.turn_for(LEFT, abs(angle_degrees), DEGREES)

def drive_straight(distance_inches, speed=60):
    Drivetrain.set_drive_velocity(speed, PERCENT)
    # FIX 3: VEX drive_for logic: Use FORWARD with positive/negative numbers
    Drivetrain.drive_for(FORWARD, distance_inches, DistanceUnits.IN)

def intake_blocks(duration_sec=1.5):
    Intake.set_velocity(100, PERCENT)
    ConveyorBelt.set_velocity(100, PERCENT)
    Intake.spin(FORWARD)
    ConveyorBelt.spin(FORWARD)
    wait(duration_sec, SECONDS)
    Intake.stop()
    ConveyorBelt.stop()

def deposit_blocks(duration_sec=1.0):
    Intake.set_velocity(100, PERCENT)
    ConveyorBelt.set_velocity(100, PERCENT)
    Intake.spin(REVERSE)
    ConveyorBelt.spin(REVERSE)
    wait(duration_sec, SECONDS)
    Intake.stop(BRAKE)
    ConveyorBelt.stop(BRAKE)

def stop_drive():
    Drivetrain.stop(BRAKE)

def vision_align(signature, target_x=158, drive_speed=15):
    vision_sensor.take_snapshot(signature)
    if vision_sensor.object_count > 0:
        obj = vision_sensor.largest_object()
        offset = obj.centerX - target_x
        while abs(offset) > 5:
            turn_power = max(10, min(30, abs(offset) / 5)) 
            if offset > 0:
                LeftMotor.spin(FORWARD, turn_power, PERCENT)
                RightMotor.spin(REVERSE, turn_power, PERCENT)
            else:
                LeftMotor.spin(REVERSE, turn_power, PERCENT)
                RightMotor.spin(FORWARD, turn_power, PERCENT)
            wait(50, MSEC)
            vision_sensor.take_snapshot(signature)
            if vision_sensor.object_count == 0:
                stop_drive()
                return False
            obj = vision_sensor.largest_object()
            offset = obj.centerX - target_x
        stop_drive()
        return True
    return False

# --- THE AUTONOMOUS ROUTINE ---

def autonomous():
    inertial_sensor.calibrate()
    print("Calibrating Inertial Sensor...")
    while inertial_sensor.is_calibrating():
        wait(25, MSEC)
    inertial_sensor.set_heading(0.0, DEGREES) 
    
    set_drive_speed(60)
    drive_straight(12.0, speed=50) 
    deposit_blocks(1.5)             
    drive_straight(-4.0, speed=50) 
    turn_to_angle(90.0) 
    
    if vision_align(BLOCK_SIG, target_x=158, drive_speed=15):
        obj = vision_sensor.largest_object()
        distance_to_drive = 10 - (obj.width / 20) 
        drive_straight(distance_to_drive, speed=30) 
        intake_blocks(1.0)
    
    turn_to_angle(0.0) 

    if vision_align(GOAL_SIG, target_x=158, drive_speed=15):
        drive_straight(30.0, speed=40) 
        deposit_blocks(1.5)           

    turn_to_angle(270.0)
    drive_straight(40.0, speed=60) 
    Drivetrain.stop(HOLD)

# --- DRIVER CONTROL (Required for Competition) ---
def user_control():
    while True:
        wait(20, MSEC)

# FIX 4: Correct Competition Initialization
competition = Competition(user_control, autonomous)
