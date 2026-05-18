from ultralytics import RTDETR

model = RTDETR('./runs/detect/train_rtdetr_resnet50/weights/best.pt')
model.val(
    data='./dataset/meta_aug.yaml',
    split='test',
    save_txt=True,
    save_conf=True,
    conf=0.1,
    name="test_aug_rtdetr_resnet50"
  )