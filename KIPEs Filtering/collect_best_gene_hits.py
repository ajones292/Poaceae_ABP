import os
import sys

# Ensure correct number of arguments
if len(sys.argv) != 3:
    print("Usage: python best_hits_extract.py <GENE> <DIRECTORY>")
    sys.exit(1)

gene_name = sys.argv[1]
base_dir = sys.argv[2]

# Create output filename dynamically based on gene name
output_file = os.path.join(base_dir, f"combined_{gene_name}_hits.fasta")

with open(output_file, 'w') as outfile:
    for species_dir in os.listdir(base_dir):
        species_path = os.path.join(base_dir, species_dir)
        pep_path = os.path.join(species_path, "final_pep_files", f"{gene_name}.fasta")

        if os.path.isdir(species_path) and os.path.isfile(pep_path):
            with open(pep_path, 'r') as infile:
                sequence_lines = []
                header_info = None

                for line in infile:
                    if line.startswith(">"):
                        if sequence_lines and header_info:
                            if species_dir.startswith("Brachypodium"):
                                label = f"{gene_name}_{species_dir}_{header_info}"
                            else:
                                # Drop the line info: keep only Genus_species
                                parts = species_dir.split("_")
                                genus_species = "_".join(parts[:2])
                                label = f"{gene_name}_{genus_species}_{header_info}"
                            
                            outfile.write(f">{label}\n")
                            outfile.writelines(sequence_lines)
                            sequence_lines = []

                        header_info = line[1:].split()[0]
                    else:
                        sequence_lines.append(line)

                # Write last sequence
                if sequence_lines and header_info:
                    if species_dir.startswith("Brachypodium"):
                        label = f"{gene_name}_{species_dir}_{header_info}"
                    else:
                        parts = species_dir.split("_")
                        genus_species = "_".join(parts[:2])
                        label = f"{gene_name}_{genus_species}_{header_info}"

                    outfile.write(f">{label}\n")
                    outfile.writelines(sequence_lines)

print(f"Concatenation complete. Output saved to: {output_file}")