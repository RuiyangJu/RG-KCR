import sys
sys.setrecursionlimit(5000)

import os
import numpy as np
from PIL import Image
import xml.etree.ElementTree as ET
from pathlib import Path
from rtmdet import RTMDet
from parseq import PARSEQ
from yaml import safe_load
from concurrent.futures import ThreadPoolExecutor
import time
import json
import glob
import subprocess
import threading

from reading_order.xy_cut.eval import eval_xml
from ndl_parser import convert_to_xml_string3
from tools.ndlkoten2tei import convert_tei


class GPUMemoryMonitor:
    def __init__(self, gpu_id=0, interval=0.05):
        self.gpu_id = gpu_id
        self.interval = interval
        self.max_memory_mb = 0
        self.running = False
        self.thread = None

    def query_memory(self):
        try:
            result = subprocess.check_output(
                [
                    "nvidia-smi",
                    f"--id={self.gpu_id}",
                    "--query-gpu=memory.used",
                    "--format=csv,noheader,nounits"
                ],
                encoding="utf-8"
            )
            return int(result.strip().split("\n")[0])
        except Exception:
            return 0

    def monitor(self):
        while self.running:
            mem = self.query_memory()
            self.max_memory_mb = max(self.max_memory_mb, mem)
            time.sleep(self.interval)

    def start(self):
        self.running = True
        self.max_memory_mb = self.query_memory()
        self.thread = threading.Thread(target=self.monitor, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread is not None:
            self.thread.join()
        self.max_memory_mb = max(self.max_memory_mb, self.query_memory())

    @property
    def peak_memory_gb(self):
        return self.max_memory_mb / 1024


def get_detector(args):
    weights_path = args.det_weights
    classes_path = args.det_classes

    assert os.path.isfile(weights_path), f"There's no weight file with name {weights_path}"
    assert os.path.isfile(classes_path), f"There's no classes file with name {classes_path}"

    detector = RTMDet(
        model_path=weights_path,
        class_mapping_path=classes_path,
        score_threshold=args.det_score_threshold,
        conf_thresold=args.det_conf_threshold,
        iou_threshold=args.det_iou_threshold,
        device=args.device
    )
    return detector


def get_recognizer(args):
    weights_path = args.rec_weights
    classes_path = args.rec_classes

    assert os.path.isfile(weights_path), f"There's no weight file with name {weights_path}"
    assert os.path.isfile(classes_path), f"There's no classes file with name {classes_path}"

    with open(classes_path, encoding="utf-8") as f:
        charobj = safe_load(f)

    charlist = list(charobj["model"]["charset_train"])

    recognizer = PARSEQ(
        model_path=weights_path,
        charlist=charlist,
        device=args.device
    )
    return recognizer


def inference_on_detector(args, inputname: str, npimage: np.ndarray, outputpath: str, issaveimg: bool = True):
    detector = get_detector(args)

    detections = detector.detect(npimage)
    classeslist = list(detector.classes.values())

    if issaveimg:
        drawimage = npimage.copy()
        pil_image = detector.draw_detections(drawimage, detections=detections)

        os.makedirs(outputpath, exist_ok=True)
        output_path = os.path.join(outputpath, f"viz_{Path(inputname).name}")
        print(f"[INFO] Saving result on {output_path}")
        pil_image.save(output_path)

    return detections, classeslist


def process(args):
    rawinputpathlist = []
    inputpathlist = []

    if args.sourcedir is not None:
        for inputpath in glob.glob(os.path.join(args.sourcedir, "*")):
            rawinputpathlist.append(inputpath)

    if args.sourceimg is not None:
        rawinputpathlist.append(args.sourceimg)

    for inputpath in rawinputpathlist:
        ext = inputpath.split(".")[-1].lower()
        if ext in ["jpg", "png", "tiff", "jp2", "tif", "jpeg", "bmp"]:
            inputpathlist.append(inputpath)

    if len(inputpathlist) == 0:
        print("Images are not found.")
        return

    if not os.path.exists(args.output):
        print("Output Directory is not found.")
        return

    print(inputpathlist)

    num_images = len(inputpathlist)
    print(f"[INFO] Number of images: {num_images}")

    recognizer = get_recognizer(args=args)

    gpu_monitor = None
    if args.device == "cuda":
        gpu_monitor = GPUMemoryMonitor(gpu_id=args.gpu_id)
        gpu_monitor.start()

    tatelinecnt = 0
    alllinecnt = 0
    alljsonobjlist = []

    image_time_records = []

    total_start_time = time.perf_counter()

    for inputpath in inputpathlist:
        image_start_time = time.perf_counter()

        pil_image = Image.open(inputpath).convert("RGB")
        npimg = np.array(pil_image)

        inputdivlist = []
        imgnamelist = []

        inputdivlist.append(npimg)
        imgnamelist.append(os.path.basename(inputpath))

        allxmlstr = "<OCRDATASET>\n"
        alltextlist = []
        resjsonarray = []

        for img, imgname in zip(inputdivlist, imgnamelist):
            img_h, img_w = img.shape[:2]

            detections, classeslist = inference_on_detector(
                args=args,
                inputname=imgname,
                npimage=img,
                outputpath=args.output,
                issaveimg=args.viz
            )

            resultobj = [dict(), dict()]
            resultobj[0][0] = list()

            for i in range(16):
                resultobj[1][i] = []

            for det in detections:
                xmin, ymin, xmax, ymax = det["box"]
                conf = det["confidence"]

                if det["class_index"] == 0:
                    resultobj[0][0].append([xmin, ymin, xmax, ymax])

                resultobj[1][det["class_index"]].append(
                    [xmin, ymin, xmax, ymax, conf]
                )

            xmlstr = convert_to_xml_string3(
                img_w,
                img_h,
                imgname,
                classeslist,
                resultobj,
                score_thr=0.3,
                min_bbox_size=5,
                use_block_ad=False
            )

            xmlstr = "<OCRDATASET>" + xmlstr + "</OCRDATASET>"
            root = ET.fromstring(xmlstr)

            eval_xml(root, logger=None)

            targetdflist = []

            with ThreadPoolExecutor(max_workers=4, thread_name_prefix="thread") as executor:
                for lineobj in root.findall(".//LINE"):
                    xmin = int(lineobj.get("X"))
                    ymin = int(lineobj.get("Y"))
                    line_w = int(lineobj.get("WIDTH"))
                    line_h = int(lineobj.get("HEIGHT"))

                    if line_h > line_w:
                        tatelinecnt += 1

                    alllinecnt += 1

                    lineimg = img[ymin:ymin + line_h, xmin:xmin + line_w, :]
                    targetdflist.append(lineimg)

                resultlines = executor.map(recognizer.read, targetdflist)
                resultlines = list(resultlines)

                alltextlist.append("\n".join(resultlines))

                for idx, lineobj in enumerate(root.findall(".//LINE")):
                    lineobj.set("STRING", resultlines[idx])

                    xmin = int(lineobj.get("X"))
                    ymin = int(lineobj.get("Y"))
                    line_w = int(lineobj.get("WIDTH"))
                    line_h = int(lineobj.get("HEIGHT"))

                    try:
                        conf = float(lineobj.get("CONF"))
                    except Exception:
                        conf = 0

                    jsonobj = {
                        "boundingBox": [
                            [xmin, ymin],
                            [xmin, ymin + line_h],
                            [xmin + line_w, ymin],
                            [xmin + line_w, ymin + line_h]
                        ],
                        "id": idx,
                        "isVertical": "true",
                        "text": resultlines[idx],
                        "isTextline": "true",
                        "confidence": conf
                    }

                    resjsonarray.append(jsonobj)

            allxmlstr += ET.tostring(root.find("PAGE"), encoding="unicode") + "\n"

        allxmlstr += "</OCRDATASET>"

        if alllinecnt > 0 and tatelinecnt / alllinecnt > 0.5:
            alltextlist = alltextlist[::-1]

        basename = os.path.basename(inputpath).split(".")[0]

        with open(os.path.join(args.output, basename + ".xml"), "w", encoding="utf-8") as wf:
            wf.write(allxmlstr)

        alljsonobj = {
            "contents": [resjsonarray],
            "imginfo": {
                "img_width": img_w,
                "img_height": img_h,
                "img_path": inputpath,
                "img_name": os.path.basename(inputpath)
            }
        }

        alljsonobjlist.append(alljsonobj)

        alljsonstr = json.dumps(alljsonobj, ensure_ascii=False, indent=2)

        with open(os.path.join(args.output, basename + ".json"), "w", encoding="utf-8") as wf:
            wf.write(alljsonstr)

        with open(os.path.join(args.output, basename + ".txt"), "w", encoding="utf-8") as wtf:
            wtf.write("\n".join(alltextlist))

        image_end_time = time.perf_counter()
        image_time = image_end_time - image_start_time

        image_time_records.append({
            "image": os.path.basename(inputpath),
            "latency_sec": round(image_time, 4)
        })

        print(f"[TIME] {os.path.basename(inputpath)}: {image_time:.4f} sec")

    with open(
        os.path.join(args.output, os.path.basename(inputpathlist[0]).split(".")[0] + "_tei.xml"),
        "wb"
    ) as wf:
        allxmlstrtei = convert_tei(alljsonobjlist)
        wf.write(allxmlstrtei)

    if gpu_monitor is not None:
        gpu_monitor.stop()

    total_end_time = time.perf_counter()

    total_time = total_end_time - total_start_time
    avg_latency = total_time / num_images
    fps = num_images / total_time

    print(f"Number of images: {num_images}")
    print(f"Total Inference Time: {total_time:.4f} sec")
    print(f"Average Inference Time: {avg_latency:.4f} sec")
    print(f"Average Inference Speed: {fps:.2f} fps")

    gpu_result = {}

    if gpu_monitor is not None:
        peak_gpu_memory_gb = gpu_monitor.peak_memory_gb
        print(f"Peak GPU Memory Used: {peak_gpu_memory_gb:.4f} GB")

        gpu_result = {
            "peak_gpu_memory_used_GB": round(peak_gpu_memory_gb, 4)
        }

    speed_result = {
        "num_images": num_images,
        "total_time_sec": round(total_time, 4),
        "avg_latency_per_image_sec": round(avg_latency, 4),
        "fps": round(fps, 2),
        **gpu_result,
        "per_image_latency": image_time_records
    }

    with open(os.path.join(args.output, "speed.json"), "w", encoding="utf-8") as f:
        json.dump(speed_result, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Arguments for NDLkotenOCR-Lite")

    parser.add_argument("--sourcedir", type=str, required=False, help="Path to image directory")
    parser.add_argument("--sourceimg", type=str, required=False, help="Path to image file")
    parser.add_argument("--output", type=str, required=True, help="Path to output directory")
    parser.add_argument("--viz", type=bool, required=False, help="Save visualized image", default=False)
    parser.add_argument("--det-weights", type=str, required=False, default="model/rtmdet-s-1280x1280.onnx")
    parser.add_argument("--det-classes", type=str, required=False, default="config/ndl.yaml")
    parser.add_argument("--det-score-threshold", type=float, required=False, default=0.3)
    parser.add_argument("--det-conf-threshold", type=float, required=False, default=0.3)
    parser.add_argument("--det-iou-threshold", type=float, required=False, default=0.3)
    parser.add_argument("--rec-weights", type=str, required=False, default="model/parseq-ndl-32x384-tiny-10.onnx")
    parser.add_argument("--rec-classes", type=str, required=False, default="config/NDLmoji.yaml")
    parser.add_argument("--device", type=str, required=False, choices=["cpu", "cuda"], default="cpu")
    parser.add_argument("--gpu-id", type=int, required=False, default=0)

    args = parser.parse_args()
    process(args)