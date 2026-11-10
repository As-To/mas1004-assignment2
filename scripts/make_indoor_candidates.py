import csv
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
TRAIN = ROOT / "data" / "starter" / "train"
OUT = ROOT / "results" / "curate"
PER_CITY = 40
BATCH = 64
IMAGE_SIZE = 224


def visual_cues(image):
    small = image.resize((32, 32)).convert("RGB")
    pixels = list(small.getdata())
    sky = 0
    green = 0
    for r, g, b in pixels:
        if b > r * 1.12 and b > g * 1.02 and b > 90:
            sky += 1
        if g > r * 1.08 and g > b * 1.05 and g > 55:
            green += 1
    gray = small.convert("L")
    values = list(gray.getdata())
    edge = sum(abs(values[i] - values[i + 1]) for i in range(len(values) - 1)) / (255 * (len(values) - 1))
    return sky / len(pixels), green / len(pixels), edge


def make_sheet(city, candidates):
    columns = 5
    cell = 210
    label_h = 42
    rows = (len(candidates) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * cell, rows * (cell + label_h)), "white")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for i, item in enumerate(candidates):
        image = Image.open(item["path"]).convert("RGB")
        image = ImageOps.fit(image, (cell, cell), method=Image.Resampling.LANCZOS)
        x = (i % columns) * cell
        y = (i // columns) * (cell + label_h)
        sheet.paste(image, (x, y))
        draw.rectangle((x, y, x + 28, y + 18), fill="black")
        draw.text((x + 5, y + 3), str(i + 1), fill="white", font=font)
        draw.text((x + 2, y + cell + 2), item["path"].stem[:30], fill="black", font=font)
        draw.text((x + 2, y + cell + 19), f"ID {item['image_id']}  score {item['score']:.3f}", fill="#444444", font=font)
    path = OUT / f"indoor_candidates_{city}.png"
    sheet.save(path)
    return path


def main():
    all_candidates = {}
    for city_dir in sorted(p for p in TRAIN.iterdir() if p.is_dir()):
        paths = sorted(city_dir.glob("*.jpg"))
        scored = []
        for path in paths:
            image = Image.open(path).convert("RGB")
            sky, green, edge = visual_cues(image)
            score = 0.70 * (1.0 - min(1.0, sky + green)) + 0.30 * edge
            image_id = path.stem.split("_", 1)[1] if "_" in path.stem else path.stem
            scored.append({"path": path, "image_id": image_id, "score": score})
        scored.sort(key=lambda item: item["score"], reverse=True)
        selected = scored[:PER_CITY]
        all_candidates[city_dir.name] = selected

        csv_path = OUT / f"indoor_candidates_{city_dir.name}.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["candidate_number", "image_id", "file", "score"])
            for number, item in enumerate(selected, 1):
                writer.writerow([number, item["image_id"], str(item["path"].relative_to(TRAIN)), f"{item['score']:.6f}"])
        make_sheet(city_dir.name, selected)

    print("Indoor-review candidate shortlist; no photos were removed.")
    for city_dir in sorted(p for p in TRAIN.iterdir() if p.is_dir()):
        total = len(list(city_dir.glob("*.jpg")))
        count = len(all_candidates[city_dir.name])
        print(f"{city_dir.name}: {count}/{total} ({100 * count / total:.2f}%)")


if __name__ == "__main__":
    main()
