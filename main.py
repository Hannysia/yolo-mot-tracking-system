import shutil
import os
import cv2
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from ultralytics import YOLO

app = FastAPI(
    title="YOLOv8 MOT Tracker API",
    description="API for detecting and tracking objects in videos",
    version="1.0"
)

model = YOLO('best.pt')

@app.get("/", include_in_schema=False)
async def read_root():
    return RedirectResponse(url="/docs")


def convert_to_compatible_format(input_path: str, output_path: str):
    """
    Recodes video into .avi (MJPEG) format, which is guaranteed to
    open with the standard Windows player.
    """
    cap = cv2.VideoCapture(input_path)
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    if fps == 0:
        fps = 30.0

    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()
    return output_path

@app.post("/predict/video", response_class=FileResponse)
async def predict_video(file: UploadFile = File(...)):

    temp_filename = f"temp_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if os.path.exists("runs"):
        shutil.rmtree("runs", ignore_errors=True)

    try:
        results = model.track(
            source=temp_filename,
            save=True,
            tracker="bytetrack.yaml",
            project="runs",
            name="detect",
            exist_ok=True
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    output_dir = os.path.join("runs", "detect")
    yolo_video_path = None
    
    if os.path.exists(output_dir):
        for f in os.listdir(output_dir):
            if f.endswith((".mp4", ".avi", ".mkv")):
                yolo_video_path = os.path.join(output_dir, f)
                break

    final_video_path = None
    if yolo_video_path:
        final_video_path = yolo_video_path.rsplit('.', 1)[0] + "_compatible.avi"
        convert_to_compatible_format(yolo_video_path, final_video_path)

    if os.path.exists(temp_filename):
        os.remove(temp_filename)

    if final_video_path and os.path.exists(final_video_path):
        return FileResponse(
            path=final_video_path, 
            media_type="video/x-msvideo", 
            filename="processed_result.avi" 
        )
    else:
        return JSONResponse(content={"error": "Processing failed"}, status_code=500)