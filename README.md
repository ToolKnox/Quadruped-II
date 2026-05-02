# 🐾 Quadruped II

A 12-DOF, 12-servo printable robot dog. ROS 1 Noetic on a Raspberry Pi 4, Arduino Nano for IMU / battery / LCD, custom power-distribution PCB, PS4-controlled.

Forked from [Stanford Pupper](https://github.com/stanfordroboticsclub/StanfordQuadruped) and [notspot](https://github.com/lnotspotl/notspot_sim_py), with extensive modifications and full ROS Noetic integration.

> **Looking for the build?** Print files, BOM, wiring diagrams and the full assembly guide live on Printables: <https://www.printables.com/model/1443108-quadruped-v06-w-code>. This repo is the **code only** — firmware for the Pi and the Nano.

---

## What's in this repo

```
Quadruped_ws/                  ROS 1 Noetic catkin workspace (runs on the Pi)
├── src/Quadruped/             Top-level launch + run_robot.py entrypoint
├── src/Quadruped_control/     Gaits, kinematics, stance/swing controllers, state machine
├── src/Quadruped_description/ URDF + meshes (used by RViz / Gazebo)
├── src/Quadruped_gazebo/      Gazebo sim launch + controller config
├── src/Quadruped_simulation/  Sim-only nodes (e.g. lidar_publisher.py)
├── src/Quadruped_utilities/   Shared helpers + Tests.py
└── src/Quadruped_hardware_interfacing/
    ├── quadruped_input_interfacing/        PS4 / keyboard input → command
    ├── quadruped_servo_interfacing/        12 servos, calibration, HardwareInterface
    └── quadruped_peripheral_interfacing/   IMU, battery voltage, 1.47" LCD

Quadruped_nano/                Arduino Nano firmware
├── quadruped_arduino/         Main sketch (.ino)
└── quadruped_peripheral_interfacing/   ElectricalMeasurements.h (pin map)

Dockerfile                     ROS Noetic image used on the Pi
Docker-compose.yaml            Run config (devices, network, volumes)
.devcontainer.json             VS Code devcontainer (matches the Docker image)
ros_entrypoint.sh              Sources the workspace before exec'ing the command
```

---

## Hardware this code targets

| Component | Notes |
| --- | --- |
| Compute | Raspberry Pi 4 (4 GB+) running Ubuntu 20.04 + ROS Noetic |
| Microcontroller | Arduino Nano (USB-serial to the Pi) |
| Servos | 12 × hobby servos, driven via PCA9685 over I²C (see `HardwareInterface.py`) |
| IMU | On the Nano — see `Quadruped_nano/quadruped_peripheral_interfacing/ElectricalMeasurements.h` |
| LCD | 1.47" SPI display (driver in `quadruped_peripheral_interfacing/scripts/LCD_1inch47.py`) |
| Battery | 4S LiPo, voltage divider sensed by the Nano |
| Controller | PS4 gamepad (Bluetooth) |

> **Pin assignments and I²C addresses are defined in source.** This README intentionally does not duplicate them — the source files are the canonical truth. See:
> - Nano pins → `Quadruped_nano/quadruped_peripheral_interfacing/ElectricalMeasurements.h`
> - Servo channels → `Quadruped_ws/src/Quadruped_hardware_interfacing/quadruped_servo_interfacing/src/quadruped_servo_interfacing/HardwareInterface.py`
> - Servo calibration offsets → `.../ServoCalibrationDefinition.py`
> - Robot-level config (link lengths, gait params) → `Quadruped_ws/src/Quadruped_control/src/quadruped_control/Config.py`

> TODO (maker): once the pin map stabilises, paste a "Pin assignments" table into this README so visitors don't have to grep the source.

---

## Install — recommended path (Docker)

The repo ships a Dockerfile and a `Docker-compose.yaml` precisely so you don't have to fight a ROS Noetic install on a fresh Pi. On the Pi, with Docker + Docker Compose installed:

```bash
git clone https://github.com/ToolKnox/Quadruped-II.git
cd Quadruped-II
docker compose up --build
```

`Docker-compose.yaml` wires through the devices the robot needs (servo I²C bus, Nano USB serial, gamepad). If a device is missing the container will start but nodes that need it will error — check `docker compose logs`.

> TODO (maker): list the exact `/dev/*` devices the compose file expects, so users know what to plug in before `up`.

### VS Code devcontainer

`.devcontainer.json` lets you open the repo in VS Code (Remote – Containers) and get the same environment as the Pi for editing / building without touching the host.

## Install — bare metal (advanced)

If you'd rather skip Docker:

1. Ubuntu 20.04 + ROS 1 Noetic Desktop-Full.
2. Create a catkin workspace and symlink (or clone) `Quadruped_ws/src/*` into it.
3. `rosdep install --from-paths src --ignore-src -r -y`
4. `catkin_make` from the workspace root.
5. `source devel/setup.bash`

> TODO (maker): list the apt + pip packages the Dockerfile installs, so bare-metal users can match it. The Dockerfile is the source of truth — keep this section in sync with it.

## Arduino Nano firmware

Open `Quadruped_nano/quadruped_arduino/quadruped_arduino.ino` in the Arduino IDE (or `arduino-cli`), select **Arduino Nano** as the board, and upload.

> TODO (maker): list the required Arduino libraries (the `#include` lines in the .ino) so users can install them via the Library Manager before compiling. Likely candidates given the hardware: an IMU driver, an SPI LCD driver, and `Wire.h`.

---

## Run

After `catkin_make` and a fresh terminal:

```bash
source devel/setup.bash
roslaunch quadruped <launch-file>.launch     # see Quadruped/launch/
```

The hands-on entry point is `Quadruped_ws/src/Quadruped/scripts/run_robot.py`, with `quadruped_driver.py` doing the gait → servo loop. Calibrate the servos before the first run:

```bash
rosrun quadruped_servo_interfacing CalibrateServos.py
```

> TODO (maker): name the actual launch file(s) and the typical PS4 button mapping.

### Simulation

`Quadruped_ws/src/Quadruped_gazebo/` and `Quadruped_simulation/` provide a Gazebo sim — useful for trying gait changes without putting torque on real servos.

> TODO (maker): paste the `roslaunch` line for the sim.

---

## Troubleshooting

- **Servos don't move.** Check the PCA9685 is on the I²C bus (`i2cdetect -y 1`), check the servo rail has 5–6 V, and check `HardwareInterface.py` for the I²C address it expects.
- **Robot drifts / leans on its own.** Re-run `CalibrateServos.py` and update `ServoCalibrationDefinition.py`.
- **No PS4 input.** Make sure the gamepad is paired (`bluetoothctl`) and the input device shows up as `/dev/input/js0`. The compose file must pass it through.
- **Nano not seen by the Pi.** Confirm the serial device (often `/dev/ttyUSB0` or `/dev/ttyACM0`) and that the user is in the `dialout` group.

---

## Credits

This codebase is a fork with significant changes on top of:

- [Stanford Pupper / StanfordQuadruped](https://github.com/stanfordroboticsclub/StanfordQuadruped) — original gait + kinematics work.
- [notspot / notspot_sim_py](https://github.com/lnotspotl/notspot_sim_py) — ROS structure inspiration.

Both upstream projects are MIT-licensed; their original copyright notices are preserved in the relevant source files.

## License

> TODO (maker): add a top-level `LICENSE` file. MIT is the natural choice for the source, since both upstreams are MIT — and required, given the fork. STLs / CAD / PCB Gerbers are distributed separately on Printables under their own licence (see the project page).

## Links

- 🛠 **Build it** — <https://www.printables.com/model/1443108-quadruped-v06-w-code>
- 🐶 **Quadruped I (simpler sibling)** — same Printables URL, scroll for the link
- 💛 **Support / get the full project files** — [Printables Club](https://www.printables.com/model/1443108-quadruped-v06-w-code#join.@TomKnox.1573)