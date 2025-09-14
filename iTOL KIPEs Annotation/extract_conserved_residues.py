import os
import csv
import sys

if len(sys.argv) != 4:
    print("Usage: python generate_itol_gradient_file.py <filtered_GENE_hits.fasta> <GENE_color_gradient_
data.txt> <species_dir_path>")
    sys.exit(1)

input_fasta = sys.argv[1]
output_txt = sys.argv[2]
species_dir_path = sys.argv[3]

# Load species directories (as a set of valid folder names)
try:
    available_species_dirs = set(os.listdir(species_dir_path))
except Exception as e:
    print(f"[ERROR] Could not read species directory: {e}")
    sys.exit(1)

def parse_fasta_headers(fasta_path):
    with open(fasta_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith(">"):
                yield line[1:]  # Skip ">"

# Store (header, ConservedResidues)
header_to_conserved = {}

# Normalize directory names for safe matching
normalized_species_dirs = {d.strip(): d for d in available_species_dirs}

for header in parse_fasta_headers(input_fasta):
    try:
        parts = header.split("_")
        gene = parts[0]

        matched_species = None
        gene_id = None

        if "Brachypodium" in header:
            for i in range(4, len(parts) + 1):
                candidate = "_".join(parts[1:i])
                if candidate in normalized_species_dirs:
                    matched_species = normalized_species_dirs[candidate]
                    gene_id = "_".join(parts[i:])
                    break
        else:
            if len(parts) >= 3:
                candidate = "_".join(parts[1:3])
                if candidate in normalized_species_dirs:
                    matched_species = normalized_species_dirs[candidate]
                    gene_id = "_".join(parts[3:])

        if not matched_species:
            print(f"[WARN] No species dir found for: {header}")
            continue

        summary_path = os.path.join(species_dir_path, matched_species, "summary.txt")
        if not os.path.isfile(summary_path):
            print(f"[WARN] summary.txt missing for {matched_species}")
            continue

        found = False
        with open(summary_path, 'r') as summary_file:
            reader = csv.DictReader(summary_file, delimiter='\t')
            for row in reader:
                if gene_id in row["ID"] and row["Gene"].startswith(gene[:3]):
                    conserved = float(row["ConservedResidues"])
                    header_to_conserved[header] = conserved
                    found = True
                    break

        if not found:
            print(f"[WARN] No valid entry found for: {header}")

    except Exception as e:
        print(f"[ERROR] Failed to process {header}: {e}")

# Write iTOL annotation file
with open(output_txt, 'w') as out:
    for header, conserved in header_to_conserved.items():
        out.write(f"{header} {conserved}\n")