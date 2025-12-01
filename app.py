import gradio as gr
from ultralytics import YOLO
import os
import shutil

# Ініціалізація моделі
model = YOLO('best.pt')

def infer_and_track(video_path):
    # Логіка очистки старих результатів
    if os.path.exists("runs"):
        shutil.rmtree("runs")
    
    # Виконуємо трекінг
    # save=True створює відеофайл з намальованими боксами
    results = model.track(
        source=video_path,
        conf=0.3,           # Поріг впевненості (відсікаємо сміття)
        iou=0.5,
        save=True,
        tracker="bytetrack.yaml",
        classes=[0]         # Тільки люди
    )
    
    # Знаходимо шлях до збереженого файлу
    # Ultralytics зберігає в runs/detect/track/
    # (назва папки може змінюватись залежно від версії, тому шукаємо динамічно)
    output_dir = results[0].save_dir
    files = os.listdir(output_dir)
    
    # Шукаємо відеофайл серед результатів
    video_file = None
    for f in files:
        if f.endswith(('.mp4', '.avi')):
            video_file = os.path.join(output_dir, f)
            break
            
    return video_file

# Створення UI
iface = gr.Interface(
    fn=infer_and_track,
    inputs=gr.Video(label="Input Video"),
    outputs=gr.Video(label="Tracked Output"),
    title="YOLOv8 MOT Tracker MVP",
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)