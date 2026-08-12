# Robotic Tracked Platform

A modular robotic tracked platform combining **3D-printed mechanical components, Arduino-based motion control, Raspberry Pi computer vision, and FlySky remote control**.

<p align="center">
  <img src="images/platform_hero.png" width="900" alt="Robotic Tracked Platform">
</p>

## Overview

This project is a remotely controlled robotic tracked platform developed as an engineering graduation project.

The platform combines mechanical design, embedded electronics, radio control, 3D printing, and computer vision in a single robotic system.

### Main technologies

- Arduino Mega 2560
- Raspberry Pi 4
- Python
- OpenCV
- FlySky FS-i6 / FS-iA6B
- BTS7960 motor drivers
- SolidWorks
- 3D printing

## Key Features

- Differential tracked drive
- Remote control via FlySky radio system
- PWM motor speed control
- Emergency stop functionality
- Two-speed transmission
- Raspberry Pi video processing
- OpenCV-based obstacle detection
- 3D-printed modular chassis

## System Overview

<p align="center">
  <img src="images/platform_infographic.png" width="900" alt="System Overview">
</p>

## Real Prototype

The platform was physically designed, 3D-printed, assembled, programmed, and tested as part of a graduation engineering project.

<p align="center">
  <img src="images/platform_real.jpeg" width="850" alt="Real prototype of the robotic tracked platform">
</p>

## Demo

A short demonstration of the robotic tracked platform during real-world testing.

▶️ [Watch the platform demonstration](media/platform_demo.mp4)

## System Architecture

The robotic platform uses a two-level control architecture.

### Low-Level Control — Arduino Mega 2560

The Arduino Mega 2560 is responsible for real-time motion control and interaction with the drive system.

Main functions:

- Receiving commands from the FlySky FS-iA6B receiver via iBus
- Processing operator input
- Generating PWM signals for the BTS7960 motor drivers
- Controlling left and right DC motors
- Differential steering
- Speed control
- Emergency stop functionality
- Transmission mode control

Control chain:

`FlySky FS-i6 → FS-iA6B → Arduino Mega 2560 → BTS7960 → DC Motors`

### High-Level Processing — Raspberry Pi 4

The Raspberry Pi 4 is responsible for video processing and computer vision.

Main functions:

- Capturing video from the camera
- Processing frames using OpenCV
- HSV-based image segmentation
- Contour detection
- Basic obstacle detection
- Displaying detected objects
- Providing a foundation for future autonomous navigation

Processing chain:

`Camera → Raspberry Pi 4 → Python / OpenCV → Obstacle Detection`

## Hardware

The platform integrates mechanical, electronic, and computing components into a single robotic system.

### Main Components

- Arduino Mega 2560
- Raspberry Pi 4 Model B
- FlySky FS-i6 transmitter
- FlySky FS-iA6B receiver
- BTS7960 motor drivers
- DC motors
- Camera
- Battery power system
- Servos
- Custom electronic control module
- 3D-printed chassis and tracked drive components

The Arduino Mega 2560 handles real-time motion control, while the Raspberry Pi 4 provides additional computing power for video processing and computer vision.

## CAD & 3D Printing

The mechanical structure of the platform was designed using SolidWorks.

The CAD development included:

- Chassis design
- Tracked drive system
- Suspension components
- Mounting elements
- Internal component layout
- Transmission components
- Assembly verification

The platform was designed with additive manufacturing in mind. Most structural components were manufactured using FDM 3D printing.

3D printing made it possible to rapidly prototype, modify, and manufacture custom mechanical components specifically for the robotic platform.

## Software

The software architecture is divided into two main components.

### Arduino Firmware

The Arduino Mega 2560 firmware is responsible for real-time control of the tracked drive system.

Main functions include:

- Reading FlySky receiver commands via iBus
- Processing throttle and steering input
- PWM motor speed control
- Differential steering
- Smooth acceleration and deceleration
- Emergency stop / safety logic
- Control of the tracked drive system

Source code:

[`src/arduino/tracked_platform_control.ino`](src/arduino/tracked_platform_control.ino)

### Raspberry Pi Computer Vision

The Raspberry Pi software is written in Python and uses OpenCV for image processing.

Main functions include:

- Camera initialization
- Real-time video capture
- Image preprocessing
- HSV-based segmentation
- Edge detection
- Contour detection
- Basic obstacle detection
- Bounding-box visualization
- FPS monitoring

Source code:

[`src/raspberry_pi/obstacle_detection.py`](src/raspberry_pi/obstacle_detection.py)

Python dependencies:

[`src/raspberry_pi/requirements.txt`](src/raspberry_pi/requirements.txt)

## Repository Structure

```text
robotic-tracked-platform/
│
├── README.md
│
├── images/
│   ├── platform_hero.png
│   ├── platform_infographic.png
│   └── platform_real.jpg
│
├── media/
│   └── platform_demo.mp4
│
└── src/
    ├── arduino/
    │   └── tracked_platform_control.ino
    │
    └── raspberry_pi/
        ├── obstacle_detection.py
        └── requirements.txt
```

## Future Improvements

Possible future development of the platform includes:

- Autonomous navigation
- Advanced obstacle avoidance
- Machine-learning-based object detection
- Visual object tracking
- Integration of ultrasonic or LiDAR sensors
- Telemetry transmission
- Remote web-based control
- Communication between Raspberry Pi and Arduino
- Automatic route planning
- Improved power management

## Author

**Adilkhan Bazarkhanov**

Instrumentation Engineering graduate with interests in robotics, embedded systems, computer vision, IoT, and 3D printing.

This repository was created and is maintained by Adilkhan Bazarkhanov as an engineering portfolio project.

## Academic Project

This repository presents the engineering implementation of a graduation project completed in 2026.

The repository is maintained as a technical portfolio demonstrating experience in:

- Robotics
- Embedded systems
- Computer vision
- 3D printing
- CAD design
- Electronics integration
- Python and OpenCV
- Arduino development
