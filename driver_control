# ============================================================
#  FINAL DRIVER CONTROL - MAIN FILE
#  VEXcode V5 (Python)
#
#  Drivetrain : PORT11/12 left, PORT13/14 right
#  Lift (DR4B): PORT10 left, PORT9 right
#               green cartridge, 1:1, mirrored gear train
#
#  Controls:
#    Left stick vertical  (axis3) - throttle
#    Right stick horiz.   (axis1) - steering
#    L1 - lift up
#    L2 - lift down
#    B + DOWN - re-home the lift
# ============================================================

from vex import *

# ---------------- BRAIN & CONTROLLER ----------------
brain = Brain()
controller = Controller()

# ---------------- DRIVETRAIN MOTORS ----------------
left_motor_a = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
left_motor_b = Motor(Ports.PORT12, GearSetting.RATIO_18_1, True)
left_drive = MotorGroup(left_motor_a, left_motor_b)

right_motor_a = Motor(Ports.PORT13, GearSetting.RATIO_18_1, False)
right_motor_b = Motor(Ports.PORT14, GearSetting.RATIO_18_1, False)
right_drive = MotorGroup(right_motor_a, right_motor_b)

# ---------------- LIFT MOTORS ----------------
# The "True" on the right motor reverses it. If the lift goes
# DOWN when you press L1, flip these booleans.
lift_left  = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
lift_right = Motor(Ports.PORT9,  GearSetting.RATIO_18_1, True)
lift = MotorGroup(lift_left, lift_right)


# ============================================================
#  TUNING CONSTANTS
# ============================================================

# ---- Drivetrain ----
DEADBAND  = 5       # ignore joystick noise below this percent
TURN_GAIN = 1.0     # raise toward 1.5 for sharper turning

# ---- Lift: protection ----
# Torque cap is the single most important protection at 1:1.
# It limits current so the motors can't sit at stall current.
# Raise in steps of 10 only if the lift genuinely cannot get
# off the ground with good rubber bands.
MAX_TORQUE_PCT = 50

# ---- Lift: soft limits (motor degrees; at 1:1 = arm degrees)
LIFT_MIN_DEG = 45      # tolerance below the homed zero
LIFT_MAX_DEG = 135      # <-- MEASURE AND REPLACE (see bottom)

# ---- Lift: speeds ----
UP_PCT   = 100          # effectively capped by MAX_TORQUE_PCT
DOWN_PCT = 40           # gravity helps; don't slam the bottom
HOLD_PCT = 10           # gentle trim to resist droop
HOLD_THRESHOLD_DEG = 15 # above this height, apply HOLD_PCT

# ---- Lift: smoothing ----
SLEW_PER_LOOP = 6       # max percent change per 20 ms loop

# ---- Lift: thermal guard (Celsius) ----
TEMP_CUTOFF_C = 50      # V5 motors self-limit near 55C
TEMP_RESUME_C = 45

# ---- Lift: stall detection ----
STALL_VEL_RPM = 5
STALL_MS      = 350

# ---- Lift: homing ----
HOMING_PCT        = 25    # gentle downward power while homing
HOMING_TORQUE_PCT = 30    # low, so we touch the stop softly
HOMING_GRACE_MS   = 300   # ignore velocity while it gets moving
HOMING_SETTLE_MS  = 250   # not moving this long = at bottom
HOMING_TIMEOUT_MS = 2500  # give up rather than grind forever

# ---- Controller screen ----
# The controller screen cannot keep up with a 20 ms loop.
# Updating it too often causes visible lag.
SCREEN_UPDATE_MS = 250


# ============================================================
#  STATE
# ============================================================
lift_cmd     = 0.0      # command actually being applied
stall_timer  = 0        # ms spent stalled
thermal_lock = False    # True = lift disabled, too hot
is_homed     = False    # has the lift found its bottom yet
screen_timer = 0        # ms since last screen update


def clamp(v, lo, hi):
    if v < lo:
        return lo
    if v > hi:
        return hi
    return v


# ============================================================
#  LIFT HOMING
#
#  Drives the lift down at low power until it stops moving
#  against its own bottom stop, then calls that zero. This
#  means the lift can start at ANY height -- you never have to
#  remember to rest it down before running the program.
# ============================================================
def lift_home():
    global lift_cmd, stall_timer, thermal_lock, is_homed

    lift.set_stopping(BRAKE)
    lift.set_max_torque(HOMING_TORQUE_PCT, PERCENT)

    controller.screen.set_cursor(1, 1)
    controller.screen.print("HOMING LIFT...    ")

    lift.spin(REVERSE, HOMING_PCT, PERCENT)

    elapsed = 0
    settled = 0
    while elapsed < HOMING_TIMEOUT_MS:
        wait(20, MSEC)
        elapsed += 20

        # Give it a moment to start moving before judging it
        # stopped, or it "finds" the bottom instantly.
        if elapsed < HOMING_GRACE_MS:
            continue

        if abs(lift.velocity(RPM)) < STALL_VEL_RPM:
            settled += 20
            if settled >= HOMING_SETTLE_MS:
                break
        else:
            settled = 0

    lift.stop()
    lift.set_position(0, DEGREES)

    # restore normal operating limits
    lift.set_max_torque(MAX_TORQUE_PCT, PERCENT)
    lift_cmd     = 0.0
    stall_timer  = 0
    thermal_lock = False
    is_homed     = True

    controller.screen.set_cursor(1, 1)
    controller.screen.print("LIFT READY        ")


def ensure_homed():
    # Homes only once per power cycle. Called at the start of
    # BOTH autonomous and driver control, because on a real
    # field the robot is disabled until a period begins --
    # motors commanded before that would go nowhere.
    if not is_homed:
        lift_home()


# ============================================================
#  LIFT CONTROL  -- called every loop
# ============================================================
def lift_control():
    global lift_cmd, stall_timer, thermal_lock, screen_timer

    # --- manual re-home: hold B + DOWN ---
    # Use if the lift gets out of sync mid-practice (someone
    # moved it by hand, a shaft slipped, etc).
    if controller.buttonB.pressing() and controller.buttonDown.pressing():
        lift_home()
        return

    pos  = lift.position(DEGREES)
    vel  = abs(lift.velocity(RPM))
    temp = max(lift_left.temperature(TemperatureUnits.CELSIUS),
               lift_right.temperature(TemperatureUnits.CELSIUS))

    # --- thermal guard (hysteresis so it doesn't chatter) ---
    if temp >= TEMP_CUTOFF_C:
        thermal_lock = True
    if thermal_lock and temp <= TEMP_RESUME_C:
        thermal_lock = False

    # --- decide target command ---
    if thermal_lock:
        target = 0                                  # let it cool
    elif controller.buttonL1.pressing() and pos < LIFT_MAX_DEG:
        target = UP_PCT
    elif controller.buttonL2.pressing() and pos > LIFT_MIN_DEG:
        target = -DOWN_PCT
    elif pos > HOLD_THRESHOLD_DEG:
        target = HOLD_PCT
    else:
        target = 0

    # --- stall protection ---
    # If we command real power and nothing moves, stop pushing.
    # This is what saves the motors and the gear teeth.
    if abs(target) > 20 and vel < STALL_VEL_RPM:
        stall_timer += 20
    else:
        stall_timer = 0

    if stall_timer > STALL_MS:
        target = clamp(target, -HOLD_PCT, HOLD_PCT)

    # --- slew limiting (no instant current spikes) ---
    if target > lift_cmd:
        lift_cmd = min(target, lift_cmd + SLEW_PER_LOOP)
    elif target < lift_cmd:
        lift_cmd = max(target, lift_cmd - SLEW_PER_LOOP)

    # --- apply ---
    if abs(lift_cmd) < 2.0:
        lift.stop()
    else:
        lift.spin(FORWARD, lift_cmd, PERCENT)

    # --- driver feedback (throttled) ---
    screen_timer += 20
    if screen_timer >= SCREEN_UPDATE_MS:
        screen_timer = 0
        controller.screen.set_cursor(1, 1)
        if thermal_lock:
            controller.screen.print("LIFT HOT - COOLING ")
        else:
            controller.screen.print(
                "Lft {:>3.0f}C P{:>4.0f}  ".format(temp, pos))


# ============================================================
#  DRIVE CONTROL  -- called every loop
# ============================================================
def drive_control():
    throttle = controller.axis3.position()
    steering = controller.axis1.position()

    # Deadband: joysticks rarely read exactly zero at rest.
    # Without this the robot creeps and the motors buzz.
    if abs(throttle) < DEADBAND:
        throttle = 0
    if abs(steering) < DEADBAND:
        steering = 0

    left_power  = throttle + (steering * TURN_GAIN)
    right_power = throttle - (steering * TURN_GAIN)

    # Scale both sides down together if either exceeds 100.
    # Plain clipping would cost you steering authority at full
    # throttle -- the robot stops turning when you need it most.
    biggest = max(abs(left_power), abs(right_power))
    if biggest > 100:
        left_power  = left_power  * 100 / biggest
        right_power = right_power * 100 / biggest

    if left_power == 0 and right_power == 0:
        left_drive.stop()
        right_drive.stop()
    else:
        left_drive.spin(FORWARD, left_power, PERCENT)
        right_drive.spin(FORWARD, right_power, PERCENT)


# ============================================================
#  DRIVER CONTROL
# ============================================================
def user_control():
    ensure_homed()

    left_drive.set_stopping(BRAKE)
    right_drive.set_stopping(BRAKE)

    while True:
        drive_control()
        lift_control()
        wait(20, MSEC)   # MUST stay inside the loop


# ============================================================
#  AUTONOMOUS
# ============================================================
def autonomous():
    ensure_homed()
    # ... your auton routine here ...
    pass


# ============================================================
#  COMPETITION
#  Must be at global scope, at the bottom of the file.
# ============================================================
competition = Competition(user_control, autonomous)


# ============================================================
#  CALIBRATION: finding LIFT_MAX_DEG
#
#  1. Set LIFT_MAX_DEG to 9999 temporarily.
#  2. Run the program and let the lift home.
#  3. Raise the lift BY HAND to its safe top position --
#     stop before anything binds or bottoms out.
#  4. Read the P value on the controller screen.
#  5. Subtract about 10 degrees for margin, put that number
#     into LIFT_MAX_DEG.
#  6. Re-run and confirm the lift stops on its own.
#
#  BANDING (matters more than any of this code at 1:1):
#  With power off, the lift should roughly balance at mid
#  height. If it slams down, add bands. If it flies up, remove
#  some. Anchor bands near the bottom pivot, offset from the
#  pivot point, so tension is highest at the bottom of travel.
#
#  Watch the temperature readout while driving. Past 40C in
#  normal use means the bands are not carrying enough load.
# ============================================================
