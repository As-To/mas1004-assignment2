from pathlib import Path

import torch
from PIL import Image, ImageDraw, ImageFont, ImageOps
from torchvision import transforms as T


ROOT = Path(__file__).resolve().parents[1]
TRAIN = ROOT / "data" / "starter" / "train"
OUT = ROOT / "results" / "curate" / "random_resized_crop_scales.png"

CELL = 224
CELL_W = 250
CELL_H = 270
LEFT = 120
TOP = 80
GAP = 8
SCALES = [(0.35, 3), (0.5, 3), (0.7, 3)]


def choose_photo(city, fraction):
    photos = sorted((TRAIN / city).glob("*.jpg"))
    if not photos:
        raise FileNotFoundError(f"No training photos found for {city}")
    return photos[min(int(len(photos) * fraction), len(photos) - 1)]


def paste_image(sheet, image, x, y):
    image = ImageOps.contain(image.convert("RGB"), (CELL, CELL))
    tile = Image.new("RGB", (CELL, CELL), "#eeeeee")
    tile.paste(image, ((CELL - image.width) // 2, (CELL - image.height) // 2))
    sheet.paste(tile, (x, y))


def main():
    selected = [
        ("Seoul", choose_photo("seoul", 0.15)),
        ("Seoul", choose_photo("seoul", 0.75)),
        ("Busan", choose_photo("busan", 0.35)),
        ("Tokyo", choose_photo("tokyo", 0.45)),
        ("Osaka", choose_photo("osaka", 0.60)),
        ("Taipei", choose_photo("taipei", 0.50)),
    ]

    columns = 1 + sum(count for _, count in SCALES)
    width = LEFT + columns * CELL_W + (columns - 1) * GAP
    height = TOP + len(selected) * CELL_H + (len(selected) - 1) * GAP
    sheet = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    bold = ImageFont.load_default()

    headers = ["Original"]
    for scale, count in SCALES:
        headers.extend([f"scale {scale:.2f}\ncrop {i}" for i in range(1, count + 1)])
    for col, header in enumerate(headers):
        x = LEFT + col * (CELL_W + GAP)
        draw.multiline_text((x + 4, 10), header, fill="#111111", font=bold, spacing=2)

    torch.manual_seed(20261031)
    for row, (city, path) in enumerate(selected):
        y = TOP + row * (CELL_H + GAP)
        draw.text((8, y + 4), city, fill="#111111", font=font)
        draw.text((8, y + 22), path.name[:17], fill="#555555", font=font)

        original = Image.open(path).convert("RGB")
        paste_image(sheet, original, LEFT, y)
        base_col = 1
        for scale, _ in SCALES:
            transform = T.RandomResizedCrop(CELL, scale=(scale, 1.0))
            for offset in range(3):
                crop = transform(original)
                x = LEFT + (base_col + offset) * (CELL_W + GAP)
                paste_image(sheet, crop, x, y)
            base_col += 3

    OUT.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(OUT)
    print(f"selected {len(selected)} photos")
    for city, path in selected:
        print(f"{city}: {path.relative_to(ROOT)}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
