import sys
import os
from collections import defaultdict

if len(sys.argv) != 2:
    print("Usage: python split_by_gene.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]
input_dir = os.path.dirname(os.path.abspath(input_file))

# Collect lines by gene prefix (before the first underscore)
gene_to_lines = defaultdict(list)

with open(input_file, 'r') as infile:
    for line in infile:
        line = line.strip()
        if not line:
            continue
        try:
            header, value = line.split()
            gene = header.split("_")[0]
            gene_to_lines[gene].append(f"{header} {value}")
        except ValueError:
            print(f"[WARN] Skipping malformed line: {line}")

# Write each gene's entries to a file in the same directory as the input
for gene, lines in gene_to_lines.items():
    output_filename = f"color_gradient_{gene}_hits.txt"
    output_path = os.path.join(input_dir, output_filename)
    with open(output_path, 'w') as outfile:
        outfile.write("\n".join(lines) + "\n")

print(f"[INFO] Split complete. Files written to: {input_dir}")