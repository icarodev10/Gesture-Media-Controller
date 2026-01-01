# 🖐️ Gesture Media Controller

> A contactless media controller powered by Computer Vision, allowing users to control system volume and media playback using simple hand gestures.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?style=for-the-badge&logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-orange?style=for-the-badge)

## 💡 About The Project

**Gesture Media Controller** creates a futuristic, touch-free interface for your PC. By leveraging **MediaPipe** for hand tracking and **OpenCV** for visual processing, this script interprets hand landmarks to interact with the Windows OS in real-time.

It was designed with a focus on **Usability Engineering**, implementing logic to prevent accidental triggers (false positives) when the user moves their hand naturally.

### Key Features

* **🔊 Volume Control:** Pinch your Thumb and Index finger to adjust Master Volume.
    * *HUD Feedback:* A neon bar indicates the volume level visually.
    * *Safe Mode:* Volume control is strictly locked unless the other fingers (Middle, Ring, Pinky) are extended upwards, preventing accidental changes when closing the hand.
* **⏭️ Next Track:** "Hang Loose" gesture (Thumb + Pinky interaction) skips to the next song.
* **⏯️ Play/Pause:** Simply close your hand (make a fist) to toggle media playback.
* **🛡️ Conflict Prevention:** Smart logic prioritizes gestures and uses a geometric "Kill Switch" to disable volume control instantly if the hand starts to close, ensuring a smooth transition between gestures.

---

## 🛠️ Technologies Used

* **Python 3.11**
* **OpenCV (cv2):** Image processing and HUD drawing.
* **MediaPipe (v0.10.21):** High-fidelity hand tracking.
* **PyCaw:** Windows Core Audio API wrapper for volume control.
* **PyAutoGUI:** Simulation of media keyboard keys.

---

## 🚀 How to Run

### Prerequisites

You need **Python 3.11** installed. This project requires specific versions of audio libraries to work on Windows 10/11.

1.  **Clone the repository:**
    
    git clone [https://github.com/icarodev10/Gesture-Media-Controller.git](https://github.com/icarodev10/Gesture-Media-Controller.git)
    cd Gesture-Media-Controller
    

2.  **Create a Virtual Environment (Optional but Recommended):**
    
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    

3.  **Install Dependencies:**
    
    pip install -r requirements.txt
    
    *(Note: Ensure `pycaw==20181226`, `comtypes==1.1.14` and `mediapipe==0.10.21` are used).*

4.  **Run the Controller:**
    
    python media_controller.py
    

---

## 🎮 Controls Guide

| Action | Gesture | Condition |
| :--- | :--- | :--- |
| **Volume Control** | Pinch (Index + Thumb) | **Only active if** Middle, Ring, and Pinky fingers are UP (Open Palm). |
| **Next Track** | Hang Loose (Pinky + Thumb) | Connect Pinky and Thumb tips. |
| **Play / Pause** | Fist (Close Hand) | Close all fingers. |

---

## 🧠 Technical Highlights (Logic)

One of the main challenges was the **"Gesture Transition Problem"**.
* *Issue:* When making a fist to Pause, the Index finger naturally approaches the Thumb, which the system initially mistook for a "Volume Down" command.
* *Solution:* Implemented a strict **"Safe Mode"**. Volume control is programmatically disabled if the Middle, Ring, or Pinky fingers are bent below their knuckles. This acts as a hardware-like safety switch, ensuring the volume never fluctuates unintentionally while performing other gestures.

---

## 👤 Author

**Icaro**
* [LinkedIn](https://www.linkedin.com/in/icaro-souza-ti/)

---