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
    save_txt=True,
    save_conf=True,
    conf=0.1,
    name=f"test_{model_name}"
)