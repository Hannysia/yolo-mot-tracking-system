# YOLOv8 MOT Tracking System

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)

A FastAPI-based application for object detection and tracking using a fine-tuned YOLOv8 model and ByteTrack algorithm. The system processes video inputs to detect pedestrians, track their IDs across frames, and output a compatible AVI video file.

## Features

* **Custom Detection:** YOLOv8n model fine-tuned on the MOT17 dataset specifically for pedestrian detection.
* **Advanced Tracking:** Implements ByteTrack for robust ID assignment and trajectory tracking, handling occlusions effectively.
* **Compatibility:** Automatically converts processed video to `.avi` (MJPEG) format to ensure playback compatibility on Windows default media players.
* **Containerization:** Fully dockerized application for consistent deployment across environments.

## Technology Stack

* **Core:** Python 3.10
* **ML/AI:** PyTorch, Ultralytics YOLOv8
* **Computer Vision:** OpenCV (Headless)
* **Backend:** FastAPI, Uvicorn

## Prerequisites

Before running the project, ensure you have the following installed:

* **Docker** (for containerized run)
* **Python 3.10+** and **Git** (for local development)

## Installation and Execution

### Option 1: Docker (Recommended)

This method requires no local Python configuration.

1.  **Pull and run the pre-built image:**
    ```bash
    docker run -p 8000:8000 anykn/yolo-mot-app:v1.0
    ```

2.  **Or build from source:**
    ```bash
    docker build -t yolo-mot-app .
    docker run -p 8000:8000 yolo-mot-app
    ```

### Option 2: Local Development

Follow these steps to run the application directly on your machine.

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd yolo-mot-tracking-system
    ```

2.  **Create and activate a virtual environment:**

    * *Windows:*
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

    * *Linux / macOS:*
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Start the server:**
    ```bash
    uvicorn main:app --reload
    ```

## Usage

1.  **Start the server.**
    Once the container or script is running, open your browser and go to:
    👉 `http://localhost:8000`
    *(You will be automatically redirected to the interactive API documentation)*.

2.  **Find the Endpoint.**
    Locate the **POST /predict/video** section and click **Try it out**.

3.  **Upload Video.**
    * You can use your own video file (`.mp4`, `.avi`, or `.mkv`).
    * **Don't have a video?** Use the `test_video.mp4` provided in this repository for a quick test.

4.  **Run Processing.**
    Click **Execute** and wait for the model to process the video.

5.  **Get Result.**
    After processing is complete, click the **Download link** in the response section to save the `processed_result.avi` file.
