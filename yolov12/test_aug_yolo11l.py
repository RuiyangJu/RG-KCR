from ultralytics import YOLO

model = YOLO('./runs/detect/train_yolo11l/weights/best.pt')
model.val(
    data='./dataset/meta_aug.yaml',
    split='test',
    save_txt=True,
    save_conf=True,
    conf=0.1,
    name="test_aug_yolo11l"
  )