import sys
import csv
from collections import defaultdict

if len(sys.argv) != 3:
    print("Usage: python convert_to_presence_absence_matrix.py <input_long_format.txt> <output_matrix.cs
v>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

data = defaultdict(dict)  # {species: {gene: value}}
genes_set = set()
species_set = set()

with open(input_file, 'r') as f:
    header = next(f)  # skip header
    for line in f:
        line = line.strip()
        if not line:
            continue

        identifier, val = line.split()
        parts = identifier.split('_')

        gene = parts[0]
        genus = parts[1]

        # Handle Brachypodium separately
        if genus == "Brachypodium":
            if len(parts) >= 5:
                # gene_Brachypodium_species_line_geneID
                species = f"{parts[1]}_{parts[2]}_{parts[3]}"
                gene_id = "_".join(parts[4:])  # handle gene IDs like XP_123456789
            else:
                print(f"[WARN] Unexpected Brachypodium format: {line}")
                continue
        else:
            if len(parts) >= 4:
                # gene_Genus_species_geneID
                species = f"{parts[1]}_{parts[2]}"
                gene_id = "_".join(parts[3:])  # again, preserve full gene ID
            else:
                print(f"[WARN] Unexpected format: {line}")
                continue

        genes_set.add(gene)
        species_set.add(species)
        data[species][gene] = val

# Sort for consistent output
genes = sorted(genes_set)
species = sorted(species_set)

with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Species"] + genes)

    for sp in species:
        row = [sp]
        for g in genes:
            row.append(data[sp].get(g, "NA"))
        writer.writerow(row)