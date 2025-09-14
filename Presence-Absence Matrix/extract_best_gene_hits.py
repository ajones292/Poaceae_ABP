import os
import csv
import sys

if len(sys.argv) != 3:
    print("Usage: python create_presence_absence_matrix.py <base_dir> <output_file>")
    sys.exit(1)

base_dir = sys.argv[1]
output_file = sys.argv[2]

species_dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

with open(output_file, 'w') as out:
    out.write("Gene_Genus_species_GeneID ConservedResidues\n")

    for species in species_dirs:
        species_path = os.path.join(base_dir, species)
        pep_dir = os.path.join(species_path, "final_pep_files")
        summary_path = os.path.join(species_path, "summary.txt")

        if not os.path.isdir(pep_dir):
            print(f"[WARN] Missing final_pep_files in {species}")
            continue
        if not os.path.isfile(summary_path):
            print(f"[WARN] Missing summary.txt in {species}")
            continue

        # Get list of genes by FASTA filenames (remove .fasta)
        genes = [f[:-6] for f in os.listdir(pep_dir) if f.endswith(".fasta")]

        # Read summary.txt into memory for faster lookups
        hits_by_gene = {gene: [] for gene in genes}
        with open(summary_path, 'r') as summary_file:
            reader = csv.DictReader(summary_file, delimiter='\t')
            for row in reader:
                gene_name = row['Gene'].split('_')[0]
                if gene_name in genes:
                    try:
                        conserved_val = float(row['ConservedResidues'])
                    except ValueError:
                        conserved_val = -1  # Handle bad values robustly
                    hits_by_gene[gene_name].append((row['ID'], conserved_val))

        for gene in genes:
            hits = hits_by_gene.get(gene, [])
            if hits:
                best_hit = max(hits, key=lambda x: x[1])
                best_id = best_hit[0].split()[0]
                best_val = best_hit[1]
            else:
                best_id = "NA"
                best_val = "NA"

            # Determine species identifier format
            parts = species.split("_")
            if species.startswith("Brachypodium") and len(parts) >= 3:
                species_label = f"{parts[0]}_{parts[1]}_{parts[2]}"
            elif len(parts) >= 2:
                species_label = f"{parts[0]}_{parts[1]}"
            else:
                species_label = species  # fallback if format unexpected

            out.write(f"{gene}_{species_label}_{best_id} {best_val}\n")