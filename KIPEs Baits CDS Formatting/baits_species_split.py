import os
import sys

def split_cds_by_species(fasta_files):
    species_files = {}  # species -> open file handle

    try:
        for fasta_file in fasta_files:
            with open(fasta_file, "r") as infile:
                current_header = None
                current_seq = []

                for line in infile:
                    if line.startswith(">"):
                        # Save previous sequence if we have one
                        if current_header and current_seq:
                            species_name = current_header.split("_", 2)[1] + "_" + current_header.split("_", 2)[2].split("_", 1)[0] \
                                if len(current_header.split("_")) >= 3 else "Unknown_species"
                            outfile = species_files.setdefault(
                                species_name,
                                open(f"{species_name}.cds.fasta", "w")
                            )
                            outfile.write(f">{current_header}\n")
                            outfile.write("".join(current_seq) + "\n")

                        # Reset for new sequence
                        current_header = line[1:].strip()
                        current_seq = []

                    else:
                        current_seq.append(line.strip())

                # Write last sequence in file
                if current_header and current_seq:
                    species_name = current_header.split("_", 2)[1] + "_" + current_header.split("_", 2)[2].split("_", 1)[0] \
                        if len(current_header.split("_")) >= 3 else "Unknown_species"
                    outfile = species_files.setdefault(
                        species_name,
                        open(f"{species_name}.cds.fasta", "w")
                    )
                    outfile.write(f">{current_header}\n")
                    outfile.write("".join(current_seq) + "\n")

    finally:
        # Close all open files
        for f in species_files.values():
            f.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} file1.fasta file2.fasta ...")
        sys.exit(1)

    fasta_files = sys.argv[1:]
    split_cds_by_species(fasta_files)