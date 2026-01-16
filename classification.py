import re
import json
import time
from pathlib import Path
import torch
from PIL import Image
from tqdm import tqdm
from transformers import AutoModel, AutoProcessor

repo_name = "SakanaAI/Metom"
device = "cuda" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float32 

ROOT_DIR = Path("./visual_crop/crops")  
OUT_DIR = Path("./classification_results")
IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}
BBOX_RE = re.compile(r"_X(\d+)_Y(\d+)_W(\d+)_H(\d+)", re.IGNORECASE)

def get_image(image_path: Path) -> Image.Image:
    return Image.open(image_path).convert("RGB")

def parse_bbox_from_name(name: str):
    m = BBOX_RE.search(name)
    if not m:
        return None
    x, y, w, h = map(int, m.groups())
    return [x, y, w, h]

def extract_topk_labels_only(out):
    labels = None
    if isinstance(out, dict):
        labels = out.get("labels", None)
        if labels is None:
            raise ValueError(f"Unexpected dict output keys: {list(out.keys())}")

    elif isinstance(out, (tuple, list)):
        if len(out) == 2 and isinstance(out[0], (list, tuple)):
            labels = out[0]
        else:
            labels = out

    else:
        labels = out

    if isinstance(labels, (list, tuple)) and len(labels) > 0 and isinstance(labels[0], (list, tuple)):
        if len(labels) == 1:
            labels = labels[0]

    if isinstance(labels, (list, tuple)) and len(labels) > 0:
        first = labels[0]
        if isinstance(first, (list, tuple)) and len(first) == 2:
            labels = [x[0] for x in labels]

    if not isinstance(labels, (list, tuple)):
        labels = [labels]

    return [str(x) for x in labels]

processor = AutoProcessor.from_pretrained(repo_name, trust_remote_code=True)
model = AutoModel.from_pretrained(
    repo_name,
    torch_dtype=torch_dtype,
    _attn_implementation="eager",
    trust_remote_code=True,
).to(device=device)
model.eval()

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    subdirs = sorted([p for p in ROOT_DIR.iterdir() if p.is_dir()])
    if not subdirs:
        raise RuntimeError(f"No subfolders found under: {ROOT_DIR}")

    t0_all = time.perf_counter()

    for folder in tqdm(subdirs, desc="Folders", unit="folder"):
        t0_folder = time.perf_counter()

        img_paths = sorted([p for p in folder.iterdir() if p.suffix.lower() in IMG_EXTS])
        results = []

        for img_path in tqdm(img_paths, desc=f"Images in {folder.name}", unit="img", leave=False):
            bbox = parse_bbox_from_name(img_path.name)
            if bbox is None:
                continue

            image = get_image(img_path)
            pixel_values = processor(images=image, return_tensors="pt")["pixel_values"].to(
                device=device, dtype=torch_dtype
            )

            with torch.inference_mode():
                out = model.get_topk_labels(pixel_values, k=5, return_probs=True)

            char_top5 = extract_topk_labels_only(out)

            char_top5 = char_top5[:5]

            results.append(
                {
                    "char": char_top5, 
                    "bbox": bbox,     
                }
            )

        out_path = OUT_DIR / f"{folder.name}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        folder_time = time.perf_counter() - t0_folder

    total_time = time.perf_counter() - t0_all
    print(f"Done. Processed {len(subdirs)} folders in {total_time:.2f}s")
    print(f"JSON saved to: {OUT_DIR}")


if __name__ == "__main__":
    main()