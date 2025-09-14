import os

# Set the path to your directory containing FASTA files
input_dir = "/vol/data/Final_Dataset/KIPEs/cds/"

# Optional: set an output directory (leave as None to overwrite originals)
output_dir = None
# output_dir = "/path/to/trimmed_files"

if output_dir:
    os.makedirs(output_dir, exist_ok=True)

# Loop over all files in the directory
for filename in os.listdir(input_dir):
    if filename.lower().endswith((".fasta", ".fa", ".fna", ".ffn", ".faa")):
        input_path = os.path.join(input_dir, filename)

        # Read and process the file
        trimmed_lines = []
        with open(input_path, "r") as infile:
            for line in infile:
                if line.startswith(">"):
                    # Split at first whitespace (space or tab) and keep only first chunk
                    header = line.split()[0]
                    trimmed_lines.append(header + "\n")
                else:
                    trimmed_lines.append(line)

        # Decide where to write the output
        if output_dir:
            output_path = os.path.join(output_dir, filename)
        else:
            output_path = input_path  # Overwrite original

        with open(output_path, "w") as outfile:
            outfile.writelines(trimmed_lines)

print("Done trimming FASTA headers.")
