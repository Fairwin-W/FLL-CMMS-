from pybricks.hubs import PrimeHub
from pybricks.robotics import DriveBase
from pybricks.parameters import Color, Button, Port, Direction, Motor, UltrasonicSensor, ColorSensor, Stop, Side, Icon
from pybricks.tools import multitask, run_task, wait
from pybricks import version

hub = PrimeHub()

armBase = Motor(Port.D)
armMid = Motor(Port.F)

left = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right = Motor(Port.B)

drive = DriveBase(left, right, wheel_diameter=90, axle_track=100)

color = ColorSensor(Port.C)

distance = UltrasonicSensor(Port.E)

def setup():
    multitask(drive.reset(), print("Version " + str(version)))
    drive.use_gyro(True)
    drive.settings(100, 55, 30, 50) #[straight_speed, straight_acceleration, turn_rate, turn_acceleration]
    hub.imu.reset_heading()
    multitask(hub.speaker.volume(50), turnArm(90, 90))

def turnArm(angle2, angle2, mode = 0, speed = 500):
    if not mode:
        multitask(armBase.run_target(speed, angle2), armMid.run_target(speed, angle2))
    elif mode == 1:
        armBase.run_target(speed, angle2)
        armMid.run_target(speed, angle2)
    else:
        armMid.run_target(speed, angle2)
        armBase.run_target(speed, angle2)

def across():
    drive.straight(200)

tasks = [print(), across()]
inputs = ["Hello world!"]
inputCount =  0
menuindex = 0

def constrain(value, minimum, maximum):
    if value < minimum:
        return minimum
    elif value > maximum:
        return maximum
    return value

def TrackLine(Distance, NewDistance=0, NewDirection=1):
    if NewDistance >= Distance:
        drive.straight(0, Stop.COAST)
        return

    if ColorSensor.color() == "White":
        NewDirection = NewDirection * -1
        while ColorSensor.color() != "White":
            drive.curve(20 * NewDirection, 1, Stop.COAST)
        drive.straight(1, Stop.COAST)
        NewDistance += 0.5

    TrackLine(Distance, NewDistance, NewDirection)

def TrackLine1(Distance, Direction=True):
    curve_direction = 20 if Direction else -20
    while NewDistance < Distance:
        if ColorSensor.color() == "White":
            drive.straight(1, Stop.COAST)
        else:
            drive.curve(curve_direction, 1, Stop.COAST)
        NewDistance += 1

def main():
    multitask(setup(), hub.speaker.beep(500))
    global menuindex, inputCount
    while menuindex < len(tasks):
        hub.display.char(menuindex)
        pressed = hub.buttons.get_pressed()
        while True:
            if Button.CENTER in pressed:
                break
            if Button.LEFT in pressed or Button.DOWN in pressed:
                menuindex -= 1
            else:
                menuindex += 1
            menuindex = constrain(menuindex, 0, len(tasks))
        try:
            multitask(tasks[menuindex](), print("Running " + tasks[menuindex].__name__))
        except TypeError
            multitask(tasks[menuindex](), print("Running " + tasks[menuindex].__name__ + " with input " + str(inputs[inputCount])))
            tasks[menuindex](inputs[inputCount])
            inputCount += 1
