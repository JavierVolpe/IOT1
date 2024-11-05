GPS-Based Tracking and Monitoring System
========================================

**Gruppe 4, IT-TEK 1B e023**

-   Emil Fabricius Schlosser
-   Javier Alejandro Volpe
-   Jonathan Steenstrup
-   Morten Hamborg Johansen

* * * * *

This repository contains the code for a GPS-based tracking and monitoring system developed as part of the first semester project for the IT Technology program at KEA. The system utilizes an ESP32 microcontroller equipped with GPS and IMU sensors to track movement, calculate distance traveled, count events based on motion (e.g., tackles in sports), and send data to Adafruit IO for visualization and monitoring.

Table of Contents
-----------------

-   [Overview](#overview)
-   [Features](#features)
-   [Hardware Requirements](#hardware-requirements)
-   [Software Requirements](#software-requirements)
-   [Installation and Setup](#installation-and-setup)
-   [Configuration](#configuration)
-   [Running the Program](#running-the-program)
-   [Client Application](#client-application)
-   [Data Visualization](#data-visualization)
-   [Acknowledgements](#acknowledgements)
-   [License](#license)

Overview
--------

The system is designed to:

-   Track GPS coordinates and calculate the total distance traveled.
-   Monitor acceleration data to count specific events (e.g., tackles in sports).
-   Measure battery voltage and report battery status.
-   Send collected data to Adafruit IO using MQTT for real-time monitoring.
-   Provide a client application to send observations to a server.

Features
--------

-   **GPS Tracking**: Collects GPS data to monitor location and calculate distance using the Haversine formula.
-   **Event Counting**: Uses an MPU6050 IMU sensor to detect and count events based on acceleration thresholds.
-   **Battery Monitoring**: Reads battery voltage and calculates battery percentage.
-   **Data Transmission**: Sends data to Adafruit IO using MQTT for visualization.
-   **Real-Time Updates**: Synchronizes with Adafruit IO for real-time data updates.
-   **Client Application**: A UDP client (`klient.py`) to send observations to a server.

Hardware Requirements
---------------------

-   **ESP32 Microcontroller** (e.g., Educaboard ESP32)
-   **GPS Module** (compatible with UART communication)
-   **MPU6050 IMU Sensor**
-   **Battery** (with voltage between 0V and 4.2V)
-   **Buzzer**
-   **LED**
-   **Resistors and Wiring** as needed for connections

Software Requirements
---------------------

-   **MicroPython** firmware installed on the ESP32
-   **Python 3.x** for running the client application (`klient.py`)
-   **Adafruit IO Account** for data visualization
-   **MQTT Library**: `umqtt_robust2` for MicroPython
-   **Additional Libraries**:
    -   `gps_bare_minimum` (GPS functions by Kevin Lindemark)
    -   `mpu6050` MicroPython driver
    -   `machine`, `time`, `math`, `_thread` modules (available in MicroPython)

Installation and Setup
----------------------

### 1\. Setting Up the ESP32

-   **Install MicroPython** on your ESP32 if not already installed.
-   **Copy the following scripts to the ESP32**:
    -   `main.py` (the main program script)
    -   `umqtt_robust2.py` (MQTT library for MicroPython)
    -   `gps_bare_minimum.py` (GPS functions)
    -   `mpu6050.py` (IMU sensor driver)

### 2\. Wiring the Hardware

-   **Connect the GPS Module** to the ESP32 UART port (default is UART 2).
-   **Connect the MPU6050 IMU Sensor** to the ESP32 I2C pins.
-   **Connect the Buzzer** to the specified PWM pin (default is GPIO 33).
-   **Connect the LED** to the specified GPIO pin (default is GPIO 15).
-   **Connect the Battery** to the ADC pin (default is GPIO 35) through a voltage divider if necessary.

### 3\. Setting Up Adafruit IO

-   **Create an Account** at Adafruit IO.
-   **Create the Following Feeds**:
    -   `distancekm` for distance data.
    -   `mapfeed` for location data (as CSV).
    -   `batteryfeed` for battery percentage.
    -   `taklinger` for event count data.
-   **Obtain Your Adafruit IO Credentials**:
    -   **Username**
    -   **AIO Key**

### 4\. Configuring the Program

-   **Update Configuration in `main.py`**:


    `# Adafruit IO Credentials
    ADAFRUIT_IO_USERNAME = 'your_username'
    ADAFRUIT_IO_KEY = 'your_aio_key'`

-   **Set Hardware Configuration** if different from defaults:


    `# Hardware Pins
    YELLOW_PIN = 15    # LED Pin
    BUZZ_PIN = 33      # Buzzer Pin
    pin_adc_bat = 35   # Battery ADC Pin`

-   **Set Program Configuration** as needed:


    `# Enable or disable data transmission
    send_battery = 1          # 1 to send battery data
    send_location_data = 1    # 1 to send location data
    send_distance = 1         # 1 to send distance data
    send_taklinger = 1        # 1 to send event count data`

-   **Update Adafruit Feed Names** if necessary:


    `distance_km_feed = 'your_username/feeds/distancekm'
    map_feed = 'your_username/feeds/mapfeed/csv'
    battery_feed = 'your_username/feeds/batteryfeed'
    taklinger_feed = 'your_username/feeds/taklinger'`

Running the Program
-------------------

1.  **Power Up the ESP32**: Ensure all sensors and modules are properly connected.
2.  **The Program Starts Automatically**: The `main.py` script will run on boot.
3.  **Monitoring Output**:
    -   Use a serial monitor (e.g., PuTTY, Thonny) to view debug messages.
    -   The LED will indicate that the program is running.
4.  **Data Transmission**:
    -   The ESP32 will collect data and send it to Adafruit IO based on configuration.
    -   Real-time data can be viewed on your Adafruit IO dashboard.

Client Application
------------------

The `klient.py` script is a UDP client that allows you to send observations to a server.

### Running the Client

1.  **Ensure Python 3.x is Installed** on your computer.

2.  **Update Server Configuration** in `klient.py` if necessary:

    `server_name = 'server_ip_address'  # Default is '10.0.0.5'
    server_port = 12000                # Default port`

3.  **Run the Script**:

    bash

    Copy code

    `python klient.py`

4.  **Usage**:

    -   **Input Player**: When prompted, enter the player number or name.
    -   **Input Observation**: Enter the observation or message to send.
    -   **Commands**:
        -   Type `start` to send a start signal to the server.
        -   Type `exit` to exit the client application.

Data Visualization
------------------

-   **Adafruit IO Dashboards**:
    -   Create dashboards in Adafruit IO to visualize the data from your feeds.
    -   Use maps, gauges, charts, and other widgets to display distance, location, battery status, and event counts.

Acknowledgements
----------------

-   **Kevin Lindemark**: For providing the `gps_bare_minimum` module for GPS functionality.
-   **Bo Hansen**: For guidance on battery voltage measurement techniques.
-   **Adafruit**: For the MQTT library and data visualization platform.
-   **IT Technology Program at KEA**: For the support and resources provided during the project.
