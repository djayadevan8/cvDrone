from droneController import DroneController
import time

drone = DroneController()

# --------------------
# ARM
# --------------------
print("Arming...")
drone.arm()
time.sleep(2)

# --------------------
# SEND INITIAL SETPOINTS
# --------------------
print("Sending initial setpoints...")
for _ in range(20):
    drone.send_velocity(0, 0, 0, 0)
    time.sleep(0.1)

# --------------------
# START OFFBOARD
# --------------------
print("Entering Offboard...")
drone.startOffboard()
time.sleep(1)

# --------------------
# TAKEOFF TO 10 METERS
# --------------------
print("Taking off...")

target_altitude = -10.0

while True:

    # Always send the setpoint first
    drone.send_velocity(0, 0, -2, 0)

    pos = drone.getLocalPosition()

    if pos is None:
        continue

    x, y, z = pos

    print(f"Altitude: {-z:.2f} m")

    if z <= target_altitude:
        break

    time.sleep(0.1)

# --------------------
# HOVER
# --------------------
print("Hovering...")

start = time.time()

while time.time() - start < 5:

    drone.send_velocity(0, 0, 0, 0)

    pos = drone.getLocalPosition()

    if pos is not None:
        x, y, z = pos
        print(f"Altitude: {-z:.2f} m")

    time.sleep(0.1)

# --------------------
# LAND
# --------------------

print("Hover complete")

# Stop sending motion
for _ in range(20):
    drone.send_velocity(0, 0, 0, 0)
    time.sleep(0.1)

# Exit Offboard
drone.setPositionMode()

# Give PX4 time to change modes
time.sleep(3)

# Command landing
drone.land()

# Wait until the vehicle is actually on the ground
time.sleep(20)

# Only then disarm
drone.disarm()
#
#print("Stopping...")

# Stop all motion
#for _ in range(20):
 #   drone.send_velocity(0, 0, 0, 0)
  #  time.sleep(0.1)

#print("Landing...")

#drone.land()

# Wait for PX4 to land
#time.sleep(15)

#print("Mission Complete!")
###