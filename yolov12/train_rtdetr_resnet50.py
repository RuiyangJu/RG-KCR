from ultralytics import RTDETR

model = RTDETR('./ultralytics/cfg/models/rt-detr/rtdetr-resnet50.yaml')

# Train the model
results = model.train(
  data='./dataset/meta_raw.yaml',
  epochs=1000, 
  batch=8, 
  imgsz=640,
  optimizer="SGD",
  lr0=0.01,
  device="0",
  name="train_rtdetr_resnet50"
)

# Evaluate model performance on the validation set
metrics = model.val()