with open("items.json", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Convert each line into a JSON object
with open("items_fixed.json", "w", encoding="utf-8") as out:
    out.write("[\n")
    for i, line in enumerate(lines):
        line = line.strip()
        if line:
            if i != 0:
                out.write(",\n")
            out.write(line)
    out.write("\n]")
[]