# Anti-Theft Password-Based Ignition System

## Overview
The **Anti-Theft Password-Based Ignition System** is a security project that prevents unauthorized vehicle ignition using **Face Recognition** and **Password Authentication**. This system integrates a **Raspberry Pi** and a **Laptop** to provide a secure and automated authentication mechanism before allowing ignition.

## Features
- **Face Recognition** for authorized users.
- **Password Authentication** as a backup method.
- **Emergency Shutdown** option for quick system disable.
- **Relay Control** to start or stop vehicle ignition.
- **User-friendly Interface** using Python and Flask.

---

## Installation
### Raspberry Pi Setup
1. **Update Raspberry Pi OS**:
   ```bash
   sudo apt update && sudo apt upgrade
   ```
2. **Install Python 3 and pip**:
   ```bash
   sudo apt install python3 python3-pip
   ```
3. **Install required Python libraries**:
   ```bash
   pip3 install RPi.GPIO requests
   ```

### Laptop Setup
1. **Install Python 3** (Ensure it's added to the PATH during installation).
2. **Install pip**:
   ```bash
   python -m ensurepip --upgrade
   ```
3. **Install OpenCV and Flask dependencies**:
   ```bash
   pip install opencv-python flask
   ```

---

## Project Setup
### On Raspberry Pi
1. Create a directory for the project:
   ```bash
   mkdir AntiTheftIgnitionSystem && cd AntiTheftIgnitionSystem
   ```
2. Place `pi_main.py` inside this directory.

### On Laptop
1. Create a directory for the project:
   ```bash
   mkdir AntiTheftIgnitionSystem && cd AntiTheftIgnitionSystem
   ```
2. Place `app.py` and `authorized_face.jpg` in this directory.
3. Update `laptop.py` to load `authorized_face.jpg` for face recognition.

---

## Running the Project
### Step 1: Start the Flask Server on the Laptop
1. Open a terminal or command prompt in the project directory.
2. Run the following command:
   ```bash
   python app.py
   ```
3. Note the IP address and port (default: `http://0.0.0.0:5000`).
4. Ensure that the **Laptop and Raspberry Pi** are on the same network.

### Step 2: Run the Raspberry Pi Script
1. Open a terminal in the Raspberry Pi project directory.
2. Run the script:
   ```bash
   python3 pi_main.py
   ```
3. The system will initialize and wait for input from the **switches**.

---

## System Controls
- **Press Switch 2** on the Raspberry Pi to trigger **Face Recognition**:
  - If the face matches `authorized_face.jpg`, the relay **activates ignition**.
  - If the face does not match, the system prompts for a **password**.
- **Press Switch 3** to reset the system state.
- **Press Switch 4** for **emergency shutdown** (with confirmation).

---

## Important Notes
- Ensure that `SERVER_URL` in `pi_main.py` is updated with the **laptop's IP address** and port.
- The `authorized_face.jpg` should be **clear and properly visible** for recognition.
- If there are issues with dependencies, verify that **Python and pip** are correctly installed on both devices.
- Keep the Raspberry Pi powered with a **reliable power source** to avoid interruptions.

---

## Project Structure
```
AntiTheftIgnitionSystem/
│-- app.py               # Flask server running on Laptop
│-- pi_main.py           # Main script running on Raspberry Pi
│-- laptop.py            # Handles face recognition
│-- authorized_face.jpg  # Image for face recognition
│-- README.md            # Project documentation
```

---

## Author
- **Suman Naidu R**   

---

## License
This project is licensed under the **MIT License**. You are free to modify and distribute it with proper attribution.

