# ------------------------------------------
# Project:      VEXcode Project - Hybrid Push Back Autonomous (API-Correct)
# Description:  VEXcode V5 Python Project
# ------------------------------------------

from vex import *

# ---------------- Brain ----------------
brain = Brain()

# ---------------- Drivetrain ----------------
LeftMotor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
RightMotor = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
Drivetrain = DriveTrain(LeftMotor, RightMotor, 12.56, 12.5, DistanceUnits.IN)

# ---------------- Intake / Conveyor ----------------
ConveyorBelt = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
Intake = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)

# ---------------- Sensors ----------------
inertial_sensor = Inertial(Ports.PORT8)
vision_sensor = Vision(Ports.PORT5)

# ---------------- Vision Signatures ----------------
BLOCK_SIG = Signature(1, 5, 500, 75, 500, 90, 500, 1.5, 0)
GOAL_SIG  = Signature(2, 40, 500, 85, 500, 95, 500, 1.5, 0)

# ---------------- Helper Functions ----------------

def set_drive_speed(speed=60):
    Drivetrain.set_drive_velocity(speed, PERCENT)
    Drivetrain.set_turn_velocity(speed * 0.7, PERCENT)

def drive_straight(distance_inches, speed=60):
    Drivetrain.set_drive_velocity(speed, PERCENT)
    if distance_inches >= 0:
        Drivetrain.drive_for(FORWARD, distance_inches, DistanceUnits.IN)
    else:
        Drivetrain.drive_for(REVERSE, abs(distance_inches), DistanceUnits.IN)

def intake_blocks(duration_sec=1.2):
    Intake.spin(FORWARD, 100, PERCENT)
    ConveyorBelt.spin(FORWARD, 100, PERCENT)
    wait(duration_sec, SECONDS)
    Intake.stop()
    ConveyorBelt.stop()

def deposit_blocks(duration_sec=1.3):
    Intake.spin(REVERSE, 100, PERCENT)
    ConveyorBelt.spin(REVERSE, 100, PERCENT)
    wait(duration_sec, SECONDS)
    Intake.stop(BRAKE)
    ConveyorBelt.stop(BRAKE)

def stop_drive():
    Drivetrain.stop(BRAKE)

# ---------------- Autonomous ----------------

def autonomous():

    # ----- Sensor Setup -----
    inertial_sensor.calibrate()
    while inertial_sensor.is_calibrating():
        wait(25, MSEC)
    inertial_sensor.set_heading(0, DEGREES)

    set_drive_speed(60)

    Drivetrain.set_stopping(BRAKE)
    Intake.set_stopping(HOLD)
    ConveyorBelt.set_stopping(HOLD)

    # ==================================================
    # PHASE 1: NEAR SIDE MATCH LOADERS → NEAR HIGH GOAL
    # ==================================================

    # Left near match loader
    Drivetrain.turn_for(LEFT, 35, DEGREES)
    drive_straight(12, speed=40)
    intake_blocks(1.2)
    drive_straight(-6, speed=40)

    # Score near high goal
    Drivetrain.turn_for(RIGHT, 70, DEGREES)
    drive_straight(16, speed=40)
    deposit_blocks(1.3)
    drive_straight(-8, speed=40)

    # Right near match loader
    Drivetrain.turn_for(RIGHT, 55, DEGREES)
    drive_straight(14, speed=40)
    intake_blocks(1.2)
    drive_straight(-6, speed=40)

    # Score same near high goal
    Drivetrain.turn_for(LEFT, 55, DEGREES)
    drive_straight(16, speed=40)
    deposit_blocks(1.3)
    drive_straight(-10, speed=40)

    # ==================================================
    # PHASE 2: FAR SIDE MATCH LOADERS → FAR HIGH GOAL
    # ==================================================

    # Rotate and cross field
    Drivetrain.turn_for(LEFT, 180, DEGREES)
    drive_straight(42, speed=60)

    # Right far match loader
    Drivetrain.turn_for(RIGHT, 45, DEGREES)
    drive_straight(16, speed=40)
    intake_blocks(1.3)
    drive_straight(-6, speed=40)

    # Score far high goal
    Drivetrain.turn_for(LEFT, 90, DEGREES)
    drive_straight(18, speed=40)
    deposit_blocks(1.3)
    drive_straight(-10, speed=40)

    # Left far match loader
    Drivetrain.turn_for(LEFT, 90, DEGREES)
    drive_straight(16, speed=40)
    intake_blocks(1.3)
    drive_straight(-6, speed=40)

    # Score same far high goal
    Drivetrain.turn_for(RIGHT, 90, DEGREES)
    drive_straight(18, speed=40)
    deposit_blocks(1.3)

    stop_drive()

# ---------------- Driver Control ----------------

def user_control():
    while True:
        wait(20, MSEC)

# ---------------- Competition ----------------
competition = Competition(user_control, autonomous)
