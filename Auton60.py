from vex import *
import math
import urandom

brain = Brain()

# ---------------- DRIVETRAIN ----------------
left_motor_a = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
left_drive = MotorGroup(left_motor_a, left_motor_b)

right_motor_a = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
right_drive = MotorGroup(right_motor_a, right_motor_b)

inertial = Inertial(Ports.PORT8)

drivetrain = SmartDrive(
    left_drive,
    right_drive,
    inertial,
    319.19,
    320,
    40,
    MM,
    1
)

# ---------------- SENSORS ----------------
distance_sensor = Distance(Ports.PORT9)

# ---------------- INTAKE + CONVEYOR ----------------
intake = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)
conveyor = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)  # ← ADDED

# ---------------- SETTINGS ----------------
drivetrain.set_drive_velocity(45, PERCENT)
drivetrain.set_turn_velocity(35, PERCENT)

intake.set_velocity(100, PERCENT)
conveyor.set_velocity(85, PERCENT)

# Field-realistic values
LOADER_APPROACH_DIST = 140
GOAL_APPROACH_DIST = 150
PUSH_DIST = 75
REVERSE_DIST = 130


# ---------------- HELPER FUNCTIONS ----------------
def drive_until_distance(target_mm, timeout=4):
    brain.timer.reset()
    drivetrain.drive(FORWARD)

    while distance_sensor.object_distance(MM) > target_mm and brain.timer.time(SECONDS) < timeout:
        wait(10, MSEC)

    drivetrain.stop()


def load_from_match_loader(intake_time=2.5):
    # Push into loader
    drivetrain.drive_for(FORWARD, PUSH_DIST, MM)

    # Intake + conveyor together
    intake.spin(FORWARD)
    conveyor.spin(FORWARD)
    wait(intake_time, SECONDS)

    intake.stop()
    conveyor.stop()

    # Reverse away cleanly
    drivetrain.drive_for(REVERSE, REVERSE_DIST, MM)


def score_on_tall_goal(time_sec=2.5):
    # Feed balls upward reliably
    intake.spin(FORWARD)
    conveyor.spin(FORWARD)
    wait(time_sec, SECONDS)

    intake.stop()
    conveyor.stop()


# ---------------- AUTONOMOUS ----------------
def autonomous():
    inertial.calibrate()
    while inertial.is_calibrating():
        wait(25, MSEC)

    inertial.set_heading(0, DEGREES)

    # ===== MATCH LOADER 1 =====
    drivetrain.turn_for(LEFT, 90, DEGREES)
    drive_until_distance(LOADER_APPROACH_DIST)
    load_from_match_loader()

    drivetrain.turn_for(RIGHT, 135, DEGREES)
    drive_until_distance(GOAL_APPROACH_DIST)
    score_on_tall_goal()
    drivetrain.drive_for(REVERSE, 300, MM)

    # ===== MATCH LOADER 2 =====
    drivetrain.turn_for(LEFT, 90, DEGREES)
    drive_until_distance(LOADER_APPROACH_DIST)
    load_from_match_loader()

    drivetrain.turn_for(RIGHT, 90, DEGREES)
    drive_until_distance(GOAL_APPROACH_DIST)
    score_on_tall_goal()
    drivetrain.drive_for(REVERSE, 300, MM)

    # ===== MATCH LOADER 3 =====
    drivetrain.turn_for(LEFT, 110, DEGREES)
    drive_until_distance(LOADER_APPROACH_DIST)
    load_from_match_loader()

    # ===== MATCH LOADER 4 =====
    drivetrain.turn_for(LEFT, 135, DEGREES)
    drive_until_distance(LOADER_APPROACH_DIST)
    load_from_match_loader()

    drivetrain.turn_for(RIGHT, 135, DEGREES)
    drive_until_distance(GOAL_APPROACH_DIST)
    score_on_tall_goal(3)

    drivetrain.turn_for(RIGHT, 110, DEGREES)
    drive_until_distance(GOAL_APPROACH_DIST)
    score_on_tall_goal(3)

    drivetrain.drive_for(REVERSE, 400, MM)


# Run autonomous
autonomous()
