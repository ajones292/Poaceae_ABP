import sys

def fasta_to_oneline(input_file, output_file):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        sequence = ""
        header = ""

        for line in infile:
            line = line.strip()
            if line.startswith(">"):
                if header and sequence:
                    outfile.write(header + "\n" + sequence + "\n")
                header = line
                sequence = ""
            else:
                sequence += line

        if header and sequence:
            outfile.write(header + "\n" + sequence + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <input_fasta> <output_fasta>")
        sys.exit(1)

    input_fasta = sys.argv[1]
    output_fasta = sys.argv[2]
    fasta_to_oneline(input_fasta, output_fasta)