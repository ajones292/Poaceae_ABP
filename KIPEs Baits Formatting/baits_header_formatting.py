import re
import sys

def reorder_fasta_headers(input_fasta, output_fasta):
    with open(input_fasta, "r") as infile, open(output_fasta, "w") as outfile:
        for line in infile:
            if line.startswith(">"):
                # Remove the '>' for parsing
                header = line[1:].strip()
                # Example: "AKV89239.1 ANR [Prunus cerasifera]"
                match = re.match(r"([^\s]+)\s+([^\s]+)\s+\[([^\]]+)\]", header)
                if match:
                    gene_id = match.group(1)
                    gene = match.group(2)
                    genus_species = match.group(3).replace(" ", "_")
                    new_header = f">{gene}_{genus_species}_{gene_id}"
                    outfile.write(new_header + "\n")
                else:
                    # Keep the header as is if it doesn't match
                    outfile.write(line)
            else:
                # Sequence line
                outfile.write(line)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} input.fasta output.fasta")
        sys.exit(1)

    reorder_fasta_headers(sys.argv[1], sys.argv[2])
