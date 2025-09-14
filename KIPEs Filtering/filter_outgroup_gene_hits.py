import os
import csv
import sys

if len(sys.argv) != 3:
    print("Usage: python filter_fls_strict.py <filtered_fasta_from_previous_script> <output_strict_fasta
>")
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

def extract_gene_species_geneid(header):
    parts = header.split("_")
    gene = parts[0]

    matched_species = None
    for i in range(len(parts), 1, -1):
        candidate = "_".join(parts[1:i])
        if candidate in available_species_dirs:
            matched_species = candidate
            break

    if not matched_species:
        return gene, None, None

    if matched_species.startswith("Brachypodium"):
        gene_id = "_".join(parts[len(matched_species.split("_")) + 1:])
    else:
        gene_id = "_".join(parts[3:])  # skip Gene_Genus_species_

    return gene, matched_species, gene_id

# Write filtered output
with open(output_fasta, 'w') as out:
    for header, sequence in parse_fasta(input_fasta):
        try:
            gene, species_dir, gene_id = extract_gene_species_geneid(header)

            if not species_dir or not gene_id:
                print(f"[WARN] Could not parse species or gene_id from header: {header}")
                continue

            summary_path = os.path.join(base_dir, species_dir, "summary.txt")
            if not os.path.isfile(summary_path):
                print(f"[WARN] Missing summary.txt for {species_dir}")
                continue

            with open(summary_path, 'r') as summary_file:
                reader = csv.DictReader(summary_file, delimiter='\t')
                for row in reader:
                    if gene_id in row["ID"] and row["Gene"].startswith(gene[:3]):
                        conserved = float(row["ConservedResidues"])

                        # Filter condition:
                        # ANS ≥ 75.0; FLS == 100.0; F3H == 100.0
                        if gene.startswith("ANS") and conserved >= 75.0:
                            keep = True
                        elif gene.startswith("FLS") and conserved == 100.0:
                            keep = True
                        elif gene.startswith("F3H") and conserved == 100.0:
                            keep = True
                        else:
                            keep = False

                        if keep:
                            out.write(f">{header}\n")
                            for i in range(0, len(sequence), 60):
                                out.write(sequence[i:i+60] + "\n")
                        else:
                            print(f"[INFO] Skipping {header}: ConservedResidues={conserved}")
                        break
                else:
                    print(f"[WARN] No matching entry in summary.txt for {header}")

        except Exception as e:
            print(f"[ERROR] Failed to process {header}: {e}")