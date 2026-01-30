import json
import argparse
from PIL import Image, ImageDraw, ImageFont

def draw_first_char_pillow(
    image_path,
    json_path,
    out_path,
    font_path,
    font_size=64,
    draw_bbox=True,
):
    img = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, font_size)

    with open(json_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    for it in items:
        chars = it.get("char", [])
        bbox = it.get("bbox", None)

        if not chars or bbox is None or len(bbox) != 4:
            continue

        text = str(chars[0])
        x, y, w, h = bbox

        cx = x + w / 2
        cy = y + h / 2

        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        tw = right - left
        th = bottom - top

        tx = int(cx - tw / 2)
        ty = int(cy - th / 2)

        if draw_bbox:
            draw.rectangle(
                [x, y, x + w, y + h],
                outline=(0, 255, 0),
                width=2
            )

        draw.text((tx, ty), text, font=font, fill=(0, 255, 0))

    img.save(out_path)
    print("Saved:", out_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Draw first Kuzushiji character and bounding boxes on image")
    parser.add_argument("--image", required=True, help="Input image path")
    parser.add_argument("--json", required=True, help="Annotation JSON path")
    parser.add_argument("--out", required=True, help="Output image path")
    parser.add_argument("--font", default="./NotoSansCJK-Regular.ttc", help="Font file path")
    parser.add_argument("--font_size", type=int, default=64, help="Font size")
    parser.add_argument("--no_bbox", action="store_true", help="Disable drawing bounding boxes")
    args = parser.parse_args()

    draw_first_char_pillow(
        image_path=args.image,
        json_path=args.json,
        out_path=args.out,
        font_path=args.font,
        font_size=args.font_size,
        draw_bbox=not args.no_bbox,
    )