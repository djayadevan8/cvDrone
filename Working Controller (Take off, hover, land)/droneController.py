from pymavlink import mavutil
import time
import math
import csv


class DroneController:

    def __init__(self, connection="udp:127.0.0.1:14540"):

        self.log = open("flight.csv", "w", newline="")
        self.writer = csv.writer(self.log)

        self.writer.writerow([
            "Time",
            "X",
            "Y",
            "Z",
            "Battery"
        ])

        self.master = mavutil.mavlink_connection(connection)
        self.master.wait_heartbeat()

        print("Heartbeat received.")
        print("Connected to Drone")

        # Request position messages at 20 Hz
        self.master.mav.request_data_stream_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_DATA_STREAM_POSITION,
            20,
            1
        )

        self.boot_time = time.time()

        self.lat = None
        self.lon = None
        self.alt = None

        self.roll = 0
        self.pitch = 0
        self.yaw = 0

        self.battery = 0

    #################################################

    def getLocalPosition(self):

        msg = self.master.recv_match(
            type="LOCAL_POSITION_NED",
            blocking=True,
            timeout=0.05
        )

        if msg is None:
            return None

        return msg.x, msg.y, msg.z

    #################################################

    def arm(self):

        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            1,
            0, 0, 0, 0, 0, 0
        )

        print("Arming...")

    #################################################

    def disarm(self):

        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            0,
            0, 0, 0, 0, 0, 0
        )

        print("Disarming")

    #################################################

    def takeoff(self, height):

        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0,
            0, 0, 0, 0,
            0, 0, height
        )

        print(f"Taking off to {height} meters")

    #################################################

    def land(self):

        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_NAV_LAND,
            0,
            0, 0, 0, 0,
            0, 0, 0
        )

        print("Landing")

    #################################################

    def startOffboard(self):

        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_DO_SET_MODE,
            0,
            1,
            6,
            0, 0, 0, 0, 0
        )

        print("Offboard Mode")

    #################################################

    def send_velocity(self, vx, vy, vz, yaw):

        time_boot_ms = int((time.time() - self.boot_time) * 1000)

        self.master.mav.set_position_target_local_ned_send(

            time_boot_ms,

            self.master.target_system,
            self.master.target_component,

            mavutil.mavlink.MAV_FRAME_LOCAL_NED,

            0b0000111111000111,

            0, 0, 0,

            vx,
            vy,
            vz,

            0, 0, 0,

            math.radians(yaw),
            0
        )

    #################################################

    def hover(self, duration):

        start = time.time()

        while time.time() - start < duration:

            self.send_velocity(0, 0, 0, self.yaw)

            self.updateTelemetry()

            print(self.getTelemetry())

            time.sleep(0.1)

    #################################################

    def updateTelemetry(self):

        msg = self.master.recv_match(blocking=False)

        if msg is None:
            return

        t = msg.get_type()

        if t == "GLOBAL_POSITION_INT":

            self.lat = msg.lat / 1e7
            self.lon = msg.lon / 1e7
            self.alt = msg.relative_alt / 1000

        elif t == "ATTITUDE":

            self.roll = math.degrees(msg.roll)
            self.pitch = math.degrees(msg.pitch)
            self.yaw = math.degrees(msg.yaw)

        elif t == "BATTERY_STATUS":

            self.battery = msg.battery_remaining

    #################################################

    def getTelemetry(self):

        return {

            "Latitude": self.lat,
            "Longitude": self.lon,
            "Altitude": self.alt,

            "Roll": self.roll,
            "Pitch": self.pitch,
            "Yaw": self.yaw,

            "Battery": self.battery

        }

    #################################################

    def flyTrack(self, length=100, speed=3):

        pos = self.getLocalPosition()

        if pos is None:
            return

        startX, _, _ = pos

        while True:

            pos = self.getLocalPosition()

            if pos is None:
                continue

            x, _, _ = pos

            if x - startX >= length:
                break

            self.send_velocity(speed, 0, 0, 0)

            self.logFlight()

            self.updateTelemetry()

            time.sleep(0.1)

        self.hover(3)

    #################################################

    def distanceTo(self, targetX, targetY, targetZ):

        pos = self.getLocalPosition()

        if pos is None:
            return float("inf")

        x, y, z = pos

        return math.sqrt(
            (targetX - x) ** 2 +
            (targetY - y) ** 2 +
            (targetZ - z) ** 2
        )

    #################################################

    def logFlight(self):

        pos = self.getLocalPosition()

        if pos is None:
            return

        x, y, z = pos

        self.writer.writerow([
            time.time(),
            x,
            y,
            z,
            self.battery
        ])

    #################################################

    def waypointReached(self, x, y, z):

        return self.distanceTo(x, y, z) < 0.5

    #################################################

    def gotoWaypoint(self, x, y, z):

        while not self.waypointReached(x, y, z):

            pos = self.getLocalPosition()

            if pos is None:
                continue

            cx, cy, cz = pos

            vx = (x - cx) * 0.5
            vy = (y - cy) * 0.5
            vz = (z - cz) * 0.5

            self.send_velocity(vx, vy, vz, 0)

            time.sleep(0.1)

        self.send_velocity(0, 0, 0, 0)

        print("Waypoint Reached")

    #################################################

    def setHome(self):

        self.home = self.getLocalPosition()

    #################################################

    def returnHome(self):

        if self.home is None:
            print("Home position not set.")
            return

        x, y, z = self.home

        self.gotoWaypoint(x, y, z)

    ###########
    def setPositionMode(self):
        self.master.set_mode("POSCTL")
        print("Switched to Position mode")