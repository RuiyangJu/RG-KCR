import argparse
from pathlib import Path
from ultralytics import YOLO, RTDETR

parser = argparse.ArgumentParser()

parser.add_argument("--model", required=True)
parser.add_argument("--data", required=True)

args = parser.parse_args()

model_name = Path(args.model).stem

if "rtdetr" in args.model.lower():
    model = RTDETR(args.model)
else:
    model = YOLO(args.model)

model.val(
    data=args.data,
    split="test",
    conf=0.1,
    iou=0.7,
    imgsz=640,
    batch=16,
    rect=True,
    max_det=300,
    save_txt=True,
    save_conf=True,
    project="./detection/runs/detect",
    name=f"test_{model_name}",
    exist_ok=True
)
