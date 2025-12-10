from vex import *
from robot-config import *

Vision = Vision(PORT5) # Might want to check the port locations

def driveForward(distance_inches, speed=50):
  LeftMotor.spin_for(DirectionType.FWD, distance_inches, DistanceUnits.IN, wait=True)
  RightMotor.spin_for(DirectionType.FWD, distance_inches, DistanceUnits.IN, wait=True)

def turnLeft(degrees, speed=30):
  LeftMotor.spin_for(DirectionType.REV, degrees/2, DistanceUnits.DEG, wait=False)
  RightMotor.spin_for(DirectionType.FWD, degrees/2, DistanceUnits.DEG, wait=True)

def intakeBlock():
  Intake.spin(DirectionType.FWD, 100, Percent)
  wait(1, SECONDS)
  Intake.stop(Brake.HOLD)

def depositBlock():
  Intake.spin(DirectionType.REV, 100, Percent)
  wait(1, SECONDS)
  Intake.stop(Brake.HOLD)

def autonomous():
  for _ in range(2):
    while Vision.count_objects() == 0:
      LeftMotor.spin(DirectionType.FWD, 20, Percent)
      RightMotor.spin(DirectionType.FWD, 20, Percent)
    LeftMotor.stop(Brake.BRAKE)
    RightMotor.stop(Brake.BRAKE)

    distanceToBlock = Vision.largest_object().width
    if distanceToBlock < 50: driveForward(6, speed=30)
    
    intakeBlock()

    target_x = 158  # How do you locate where the goalposts are
    while True:
      obj = Vision.largest_object()
      if obj.x_position < target_x - 5:
        leftMotor.spin(FWD, 20, Percent)
        rightMotor.spin(FWD, 10, Percent)
      elif obj.x_position > target_x + 5:
        leftMotor.spin(FWD, 10, Percent)
        rightMotor.spin(FWD, 20, Percent)
      else:
          stop_motors()
          break
autonomous()
