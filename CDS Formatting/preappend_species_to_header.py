import os

# Set the directory containing your CDS FASTA files
input_dir = "/vol/data/Final_Dataset/KIPEs/cds/"

# Optional: output_dir = None to overwrite originals, or set a path to save edited files
output_dir = None
# output_dir = "/path/to/modified_files"

if output_dir:
    os.makedirs(output_dir, exist_ok=True)

# Loop through each file in the directory
for filename in os.listdir(input_dir):
    if filename.lower().endswith((".fasta", ".fa", ".fna", ".ffn", ".faa")):
        input_path = os.path.join(input_dir, filename)

        # Extract the prefix from the filename (everything before ".cds.fasta")
        if filename.lower().endswith(".cds.fasta"):
            prefix = filename[:-len(".cds.fasta")]
        else:
            prefix = os.path.splitext(filename)[0]  # fallback for non-standard endings

        # Process the file
        modified_lines = []
        with open(input_path, "r") as infile:
            for line in infile:
                if line.startswith(">"):
                    # Remove ">" and strip spaces
                    header = line[1:].strip()
                    # Prepend prefix
                    new_header = f">{prefix}_{header}\n"
                    modified_lines.append(new_header)
                else:
                    modified_lines.append(line)

        # Decide output path
        if output_dir:
            output_path = os.path.join(output_dir, filename)
        else:
            output_path = input_path

        # Write modified content
        with open(output_path, "w") as outfile:
            outfile.writelines(modified_lines)

print("Done prepending Genus_species to FASTA headers.")