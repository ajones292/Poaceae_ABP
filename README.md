# 20250906_v1_PoaceaeAnthos Scripts
Python and R scripts that were used in the preparation and construction of phylogenetic trees, as well as in the creation of presence-absence matrices. Scripts are organized into folders based on their general utilization.
## KIPEs Baits Formatting
A collection of Python scripts used to process and manipulate FASTA files containing CDS sequences for ANR, DFR, LAR, ANS, FLS, and F3H.
### `preappend_species_to_header.py`
Reads file name and preappends Genus_species identifiers to FASTA headers
### `fasta_to_oneline.py`
Converts multi-line FASTA sequences to single-line format
### `trim_header.py`
Trims FASTA headers to achieve a normalized Genus_species_GeneID format
### `combine_gene_cds_directories.py`
Merges FASTA files from separate directories containing sequences from the same species
### `remove_gene_from_header.py`
Removes gene name from FASTA headers
