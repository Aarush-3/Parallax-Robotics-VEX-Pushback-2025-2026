from vex import *
from robot-config import *

Drivetrain = DriveTrain(LeftMotor, RightMotor, 12.56, 12.5, DistanceUnits.INCHES)

# Intake/Conveyor System
ConveyorBelt = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
Intake = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)

# Sensors
inertial_sensor = Inertial(Ports.PORT8)
vision_sensor = Vision(Ports.PORT5) # Ensure this is the correct port

# --- 3. VISION SIGNATURE SETUP ---
# NOTE: You MUST train these signatures in the VEXcode V5 Utility first!
# Assumes you have trained two signatures:
BLOCK_SIG = vision_sensor.signatures.SIG_1  # For the Blocks
GOAL_SIG = vision_sensor.signatures.SIG_2   # For the Goalpost structure

# --- 4. IMPROVED MOVEMENT AND ACTION FUNCTIONS ---

def set_drive_speed(speed=60):
    """Sets consistent speed for all drivetrain commands."""
    Drivetrain.set_drive_velocity(speed, PERCENT)
    Drivetrain.set_turn_velocity(speed * 0.7, PERCENT) # Slower turns for precision

def turn_to_angle(angle_degrees, speed=40):
    """Turns accurately using the Inertial Sensor."""
    # Use the inertial sensor for precise turning
    Drivetrain.set_turn_velocity(speed, PERCENT)
    Drivetrain.turn_to_heading(angle_degrees, DEGREES)

def drive_straight(distance_inches, speed=60):
    """Drives a specific distance precisely."""
    Drivetrain.set_drive_velocity(speed, PERCENT)
    Drivetrain.drive_for(FWD, distance_inches, INCHES)

def intake_blocks(duration_sec=1.5):
    """Runs the intake and conveyor system to collect blocks."""
    # Run both motors forward to collect
    Intake.set_velocity(100, PERCENT)
    ConveyorBelt.set_velocity(100, PERCENT)
    Intake.spin(FWD)
    ConveyorBelt.spin(FWD)
    wait(duration_sec, SECONDS)

def deposit_blocks(duration_sec=1.0):
    """Reverses the system to deposit blocks into the goal."""
    # Run both motors backward to score
    Intake.set_velocity(100, PERCENT)
    ConveyorBelt.set_velocity(100, PERCENT)
    Intake.spin(REV)
    ConveyorBelt.spin(REV)
    wait(duration_sec, SECONDS)
    Intake.stop(BRAKE)
    ConveyorBelt.stop(BRAKE)

def stop_drive():
    Drivetrain.stop(BRAKE)

def vision_align(signature, target_x=158, drive_speed=15):
    """
    Uses the Vision Sensor to align the robot to a target (Block or Goal).
    Returns True if aligned, False if target is not found.
    """
    vision_sensor.take_snapshot(signature)
    
    if vision_sensor.object_count > 0:
        obj = vision_sensor.largest_object()
        offset = obj.centerX - target_x
        
        # Turn until centered (within +/- 5 pixels)
        while abs(offset) > 5:
            turn_power = max(10, min(30, abs(offset) / 5)) 
            
            if offset > 0:
                # Turn Right
                Drivetrain.stop(BRAKE)
                LeftMotor.spin(FWD, turn_power, PERCENT)
                RightMotor.spin(REV, turn_power, PERCENT)
            else:
                # Turn Left
                Drivetrain.stop(BRAKE)
                LeftMotor.spin(REV, turn_power, PERCENT)
                RightMotor.spin(FWD, turn_power, PERCENT)
                
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

# --- 5. THE AUTONOMOUS ROUTINE ---

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
    
    Drivetrain.set_drive_velocity(20, PERCENT)
    Drivetrain.drive(FWD)
    
    if vision_align(BLOCK_SIG, target_x=158, drive_speed=15):
        stop_drive()
        
        obj = vision_sensor.largest_object()

        distance_to_drive = 10 - (obj.width / 20) 
        drive_straight(distance_to_drive, speed=30) 
        
        intake_blocks(1.0)
    
    # 1. Turn towards the Center Goal (The heading of 0 should be the starting direction)
    turn_to_angle(0.0) 

    # 2. Align to the GOAL_SIG
    if vision_align(GOAL_SIG, target_x=158, drive_speed=15):
        drive_straight(30.0, speed=40) 
        deposit_blocks(1.5)           

    turn_to_angle(270.0)
    drive_straight(40.0, speed=60) 

    Drivetrain.stop(HOLD)
    print("Autonomous Routine Complete.")
