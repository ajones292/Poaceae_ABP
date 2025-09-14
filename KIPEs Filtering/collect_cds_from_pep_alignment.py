import glob
import os

aa_alignment = "/vol/data/Final_Dataset/KIPEs/gene_trees/2-ODD/alignment/mafft/baits_filtered_2-ODD_hits
_mafft.fasta"
cds_dir = "/vol/data/Final_Dataset/KIPEs/cds/"
output_file = "/vol/data/Final_Dataset/KIPEs/2-ODD_CDS.fasta"

# Load peptide headers
peptides = []
with open(aa_alignment) as aa:
    for line in aa:
        if line.startswith(">"):
            peptides.append(line[1:].strip())

found_ids = set()

def get_genus_species(header):
    # Return first two parts (Genus_species) for most
    parts = header.split("_")
    if parts[0] == "Brachypodium":
        # Brachypodium has 3 parts for species name, e.g. Brachypodium_distachyon_Bd21
        return "_".join(parts[:3])
    else:
        return "_".join(parts[:2])

found_count = 0

with open(output_file, "w") as out_handle:
    for peptide_header in peptides:
        genus_species = get_genus_species(peptide_header)
        species_cds_files = glob.glob(os.path.join(cds_dir, f"{genus_species}*.cds.fasta"))
        matched = False

        for cds_file in species_cds_files:
            with open(cds_file) as f:
                write_record = False
                current_header = ""
                for line in f:
                    if line.startswith(">"):
                        current_header = line[1:].strip()
                        if peptide_header in current_header:
                            write_record = True
                            found_ids.add(peptide_header)
                            out_handle.write(line)
                            found_count += 1
                            print(f"Found {found_count}: {peptide_header}")
                            matched = True
                        else:
                            write_record = False
                    else:
                        if write_record:
                            out_handle.write(line)
            if matched:
                break  # stop after first match found

missing_ids = set(peptides) - found_ids
if missing_ids:
    print("\nCDS sequence not found for these peptide headers:")
    for mid in sorted(missing_ids):
        print(mid)
else:
    print("\nAll peptide sequences had matching CDS sequences.")

print(f"\nExtracted CDS saved to {output_file}")