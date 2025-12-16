import gradio as gr
from ultralytics import YOLO
import os
import shutil

model = YOLO('best.pt')

def infer_and_track(video_path):
    if os.path.exists("runs"):
        shutil.rmtree("runs")
    
    results = model.track(
        source=video_path,
        conf=0.3,           
        iou=0.5,
        save=True,
        tracker="bytetrack.yaml",
        classes=[0]         
    )
    
    output_dir = results[0].save_dir
    files = os.listdir(output_dir)
    
    video_file = None
    for f in files:
        if f.endswith(('.mp4', '.avi')):
            video_file = os.path.join(output_dir, f)
            break
            
    return video_file

iface = gr.Interface(
    fn=infer_and_track,
    inputs=gr.Video(label="Input Video"),
    outputs=gr.Video(label="Tracked Output"),
    title="YOLOv8 MOT Tracker MVP",
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)