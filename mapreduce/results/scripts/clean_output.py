# clean_output.py

input_file = "mapreduce/results/raw/output.txt"
output_file = "mapreduce/results/cleaned/output_cleaned.txt"

with open(input_file, "r", encoding="latin-1") as f:
    content = f.read()

# Decode unicode escape sequences like \u00e1 → á
decoded = content.encode().decode("unicode_escape")

with open(output_file, "w", encoding="utf-8") as f:
    f.write(decoded)

print(f"✅ Cleaned output saved to: {output_file}")
