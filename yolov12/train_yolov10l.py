from ultralytics import YOLO

model = YOLO('./ultralytics/cfg/models/v10/yolov10l.yaml')

# Train the model
results = model.train(
  data='./dataset/meta_raw.yaml',
  epochs=1000, 
  batch=16, 
  imgsz=640,
  optimizer="SGD",
  lr0=0.01,
  device="0",
  name="train_yolov10l"
)

# Evaluate model performance on the validation set
metrics = model.val()