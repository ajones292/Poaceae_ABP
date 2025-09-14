import os

# Set the directory containing your CDS FASTA files
input_dir = "/vol/data/Final_Dataset/KIPEs/baits_cds/"

# Optional: None = overwrite originals
output_dir = None
# output_dir = "/path/to/renamed_files"

if output_dir:
    os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.lower().endswith((".fasta", ".fa", ".fna", ".ffn", ".faa")):
        input_path = os.path.join(input_dir, filename)

        modified_lines = []
        with open(input_path, "r") as infile:
            for line in infile:
                if line.startswith(">"):
                    header = line[1:].strip()  # remove ">"
                    # Remove the first chunk before the first underscore
                    if "_" in header:
                        header = header.split("_", 1)[1]
                    modified_lines.append(f">{header}\n")
                else:
                    modified_lines.append(line)

        if output_dir:
            output_path = os.path.join(output_dir, filename)
        else:
            output_path = input_path

        with open(output_path, "w") as outfile:
            outfile.writelines(modified_lines)

print("Done removing the first prefix from FASTA headers.")