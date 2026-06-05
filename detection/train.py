import argparse
from pathlib import Path
from ultralytics import YOLO, RTDETR

parser = argparse.ArgumentParser()
parser.add_argument("--model", required=True)
parser.add_argument("--data", required=True)

args = parser.parse_args()

model_name = Path(args.model).stem
run_name = f"train_{model_name}"

if "rtdetr" in model_name.lower():
    model = RTDETR(args.model)
else:
    model = YOLO(args.model)

results = model.train(
    data=args.data,
    epochs=1000,
    batch=16,
    imgsz=640,
    optimizer="SGD",
    lr0=0.01,
    device="0",
    name=run_name,
)

metrics = model.val()