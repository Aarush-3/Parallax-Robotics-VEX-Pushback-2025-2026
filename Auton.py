
# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode V5 Python Project
# 
# ------------------------------------------
# --- Helper Functions ---
from vex import *
from totalmain import *


def run_intake(speed_pct, duration_ms=0):
    IntakeMain.psin(FORWARD, speed_pct, PERCENT)
    IntakePortD.spin(FORWARD, speec_pct, PERCENT)
    ConveyorBelt.spin(FORWARD, speed_pct, PERCENT)
    if duration_ms > 0:
        wait(duration_ms, MSEC)

def stop_intake():
    IntakeMain.stop(BrakeType.HOLD)
    IntakePortD.stop(BrakeType.HOLD)
    ConveyerBelt.stop(BrakeType.HOLD)

def score_sequence():
    IntakeMain.spin(REVERSE, 100, PERCENT)
    IntakePortD.spin(REVERSE, 100, PERCENT)
    ConveyorBelt.spin(REVERSE, 100, PERCENT)
    wait(1500, MSEC)
    stop_intake()

# --- Functions ---

def autonomous():
    Drivetrain.set_drive_velocity(60, PERCENT)
    Drivetrain.set_turn_velocity(40, PERCENT)
    Drivetrain.drive_for(FORWARD, 14, INCHES)
    score_sequence()
    Drivetrain.drive_for(REVERSE, 10, INCHES)
    Drivetrain.turn_for(RIGHT, 90, DEGREES)
    run_intake(100)
    Drivetrain.drive_for(FORWARD, 24, INCHES)
    Drivetrain.turn_for(LEFT, 45, INCHES)
    Drivetrain.drive_for(FORWARD, 20 INCHES)
    score_sequence()
    Drivetrain.drive_for(REVERSE, 5, INCHES)
    stop_intake()
