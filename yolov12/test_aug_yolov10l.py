from ultralytics import YOLO

model = YOLO('./runs/detect/train_yolov10l/weights/best.pt')
model.val(
    data='./dataset/meta_aug.yaml',
    split='test',
    save_txt=True,
    save_conf=True,
    conf=0.1,
    name="test_aug_yolov10l"
  )