from ultralytics import YOLO

model = YOLO('./runs/detect/train_yolov9c/weights/best.pt')
model.val(
    data='./dataset/meta_raw.yaml',
    split='test',
    save_txt=True,
    save_conf=True,
    conf=0.1,
    name="test_raw_yolov9c"
  )