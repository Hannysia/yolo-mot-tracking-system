# **YOLOv8 MOT Tracking System**

System for object detection and tracking based on YOLOv8 (fine-tuned on MOT17) and ByteTrack.
Wrapped in FastAPI and containerized with Docker.

## **Features**

Custom Model: YOLOv8n fine-tuned on MOT17 dataset (Pedestrian detection).

Tracker: ByteTrack algorithm for stable ID assignment.

Robust Output: Automatically converts video to .avi (MJPEG) for maximum compatibility with Windows players.

Easy Deploy: One-command setup via Docker.

## **Tech Stack**

ML: PyTorch, Ultralytics YOLOv8

Backend: FastAPI, Uvicorn

Containerization: Docker (Python 3.10-slim)

## **How to Run (Docker)**

You don't need to install Python or CUDA. Just use Docker.

1. Build the Image

docker build -t yolo-mot-app .


2. Run the Container

docker run -p 8000:8000 yolo-mot-app


3. Usage

Open your browser and go to:
👉 http://localhost:8000/docs

Click on POST /predict/video.

Click Try it out.

Upload your video file (mp4/avi).

Click Execute and download the processed result.


**Local Development (No Docker)**

If you want to run it without Docker:

Create venv and install dependencies:

pip install -r requirements.txt


Run server:

uvicorn main:app --reload