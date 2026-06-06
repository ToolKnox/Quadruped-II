# Quadruped II assembly guide

> Draft generated from the Maker Portal software steward on 2026-06-06.
> Review dimensions, hardware choices, and safety notes before publishing externally.

## Overview

Printable Quadruped Robot
Step by Step assembly instruction.
With code

Tags: motor, robot, arduino, joystick, electronics, controller, robotics, code, quadruped, quadrupedrobot, rasberrypi, roboticsproject

## Repository contents

- `bom.csv` - bill of materials exported from the Maker Portal (96 rows at generation time).
- source/code files - firmware or helper code when available.
- printable/source files - CAD/STL/3MF/source assets when available.

## Before you build

1. Read the full README first.
2. Check the BOM and collect all hardware before printing or assembly.
3. Print structural parts with enough perimeters/infill for the expected load.
4. Dry-fit moving parts before final tightening.
5. Keep wiring accessible until the first successful power-on test.

## Assembly outline

1. **Print and inspect parts**
   - Print all required mechanical pieces.
   - Remove supports and clean holes/slots carefully.
   - Test-fit bearings, fasteners, and shafts before forcing parts together.

2. **Prepare electronics**
   - Verify board orientation and pin labels against the code.
   - Route servo/motor wiring so moving joints cannot pinch cables.
   - Do not connect batteries until continuity and polarity checks pass.

3. **Mechanical assembly**
   - Build one subsystem at a time.
   - Keep screws loose until alignment is confirmed, then tighten gradually.
   - Check that all moving sections travel freely without binding.

4. **Firmware/code upload**
   - Open the project code in the relevant IDE/toolchain.
   - Select the correct board and port.
   - Upload firmware, then test with low power or unloaded movement first.

5. **Calibration and test**
   - Center servos / zero axes before attaching horns or linkages.
   - Run a short functional test.
   - Watch for overheating motors, stalled servos, loose fasteners, or unstable power.

## Troubleshooting

| symptom | likely cause | check |
|---|---|---|
| no power | polarity, switch, battery, regulator | verify voltage at each stage |
| upload fails | wrong board/port/library | check IDE settings and cable |
| movement reversed | motor/servo orientation | swap direction in code or wiring |
| jitter/brownout | weak power supply | use adequate current and common ground |
| binding | print tolerance or fastener alignment | loosen, realign, ream/clean holes |

## Publishing checklist

- [ ] README reviewed
- [ ] `bom.csv` reviewed
- [ ] assembly photos/screenshots added if available
- [ ] printable/source files confirmed
- [ ] release package created with assets
- [ ] external platform listing updated
