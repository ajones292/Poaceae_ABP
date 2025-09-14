import os
import csv
import sys

if len(sys.argv) != 3:
    print("Usage: python deduplicate_by_conserved_residues.py <combined_GENE_FAMILY_hits.fasta> <filtere
d_GENE_FAMILY_hits.fasta>")
    sys.exit(1)

input_fasta = sys.argv[1]
output_fasta = sys.argv[2]

base_dir = os.path.dirname(os.path.abspath(input_fasta))
available_species_dirs = set(os.listdir(base_dir))

def parse_fasta(fasta_path):
    with open(fasta_path, 'r') as file:
        header, seq = None, []
        for line in file:
            line = line.strip()
            if line.startswith(">"):
                if header:
                    yield (header, ''.join(seq))
                header = line[1:]
                seq = []
            else:
                seq.append(line)
        if header:
            yield (header, ''.join(seq))

# Dictionary: gene_id (without gene name) -> (conserved_score, full_header, sequence)
best_hits = {}

for header, sequence in parse_fasta(input_fasta):
    try:
        parts = header.split("_")
        gene = parts[0]

        matched_species = None
        for i in range(len(parts), 1, -1):
            candidate = "_".join(parts[1:i])
            if candidate in available_species_dirs:
                matched_species = candidate
                break

        if not matched_species:
            print(f"[WARN] No species directory found for: {header}")
            continue

        # Determine species and gene_id based on Brachypodium logic
        if matched_species.startswith("Brachypodium"):
            gene_id = "_".join(parts[len(matched_species.split("_")) + 1:])
        else:
            gene_id = "_".join(parts[3:])  # skip Gene_Genus_species_

        summary_path = os.path.join(base_dir, matched_species, "summary.txt")

        if not os.path.isfile(summary_path):
            print(f"[WARN] summary.txt missing for {matched_species}")
            continue

        found = False
        with open(summary_path, 'r') as summary_file:
            reader = csv.DictReader(summary_file, delimiter='\t')
            for row in reader:
                if gene_id in row["ID"] and row["Gene"].startswith(gene[:3]):
                    conserved = float(row["ConservedResidues"])
                    if conserved >= 75.0:
                        id_key = f"{matched_species}_{gene_id}"  # Unique key for deduplication
                        if id_key not in best_hits or conserved > best_hits[id_key][0]:
                            best_hits[id_key] = (conserved, header, sequence)
                    else:
                        print(f"[INFO] Skipping {header}: ConservedResidues={conserved}")
                    found = True
                    break

            if not found:
                print(f"[WARN] No valid gene match for: {header}")

    except Exception as e:
        print(f"[ERROR] Failed to process {header}: {e}")

# Write deduplicated FASTA
with open(output_fasta, 'w') as out:
    for conserved, header, sequence in best_hits.values():
        out.write(f">{header}\n")
        for i in range(0, len(sequence), 60):
            out.write(sequence[i:i+60] + "\n")