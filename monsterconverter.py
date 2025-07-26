import json

INPUT_FILE = "monsters.txt"
OUTPUT_FILE = "donjon_monsters.json"

def parse_monsters(file_path):
    monsters = []
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        if not line.strip() or line.startswith("Name"):  # Skip headers or empty lines
            continue

        # Split by tabs or multiple spaces (Donjon format often uses tabs)
        parts = [p.strip() for p in line.split("\t") if p.strip()]
        if len(parts) < 8:
            parts = [p.strip() for p in line.split("  ") if p.strip()]
        if len(parts) < 8:
            continue  # Malformed line

        name, size, mtype, tags, alignment, cr, xp, source = (parts + [""] * 8)[:8]

        monster = {
            "name": name,
            "size": size,
            "type": mtype,
            "tags": tags.split(",") if tags else [],
            "alignment": alignment,
            "challenge_rating": cr,
            "xp": int(xp) if xp.isdigit() else xp,
            "source": source
        }
        monsters.append(monster)

    return monsters

def save_json(data, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    data = parse_monsters(INPUT_FILE)
    print(f"✅ Parsed {len(data)} monsters.")
    save_json(data, OUTPUT_FILE)
    print(f"📄 Saved to {OUTPUT_FILE}")
