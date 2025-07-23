import os
import json
from ultralytics import YOLO
os.environ["PYTORCH_JIT_LOG_LEVEL"] = "ERROR"

MODEL_PATH = 'yolov8n.pt'
DATA_DIR = 'data/telegram_images'
OUTPUT_PATH = 'data/image_detections.json'

def find_images(data_dir):
    image_paths = []
    for channel in os.listdir(data_dir):
        channel_dir = os.path.join(data_dir, channel)
        if os.path.isdir(channel_dir):
            for fname in os.listdir(channel_dir):
                if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
                    image_paths.append({
                        "channel": channel,
                        "image_path": os.path.join(channel_dir, fname)
                    })
    return image_paths

def main():
    try:
        model = YOLO(MODEL_PATH)
        image_paths = find_images(DATA_DIR)
        detections = []

        for img_info in image_paths:
            results = model(img_info["image_path"])
            for result in results:
                names = result.names
                for box in result.boxes:
                    detection = {
                        "channel": img_info["channel"],
                        "image_path": img_info["image_path"],
                        "detected_object_class": names[int(box.cls)],
                        "confidence_score": float(box.conf),
                    }
                    detections.append(detection)

        with open(OUTPUT_PATH, "w") as f:
            json.dump(detections, f, indent=2)

        print(f"Detections saved to {OUTPUT_PATH}")
    except Exception as e:
        pass
if __name__ == "__main__":
    main()