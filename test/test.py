from ultralytics import YOLO
model = YOLO('yolov8n.pt')
results = model('data/telegram_images/CheMed123/photo_2022-09-05_09-57-09.jpg')
print(results)