# 20250906_v1_PoaceaeAnthos Scripts
Python and R scripts that were used in the preparation and construction of phylogenetic trees, as well as in the creation of presence-absence matrices. Scripts are organized into folders based on their general utilization.
## KIPEs Baits Formatting
A collection of Python scripts used to process and format KIPEs bait files
### `bait_header_formatting.py`
Reformats headers in FASTA file from >GeneID_Gene_[Genus_species] to >Gene_Genus_species_GeneID
### `baits_species_split.py`
Splits multi-species FASTA files into separate files for each species
## CDS Formatting
A collection of Python scripts used to process and manipulate FASTA files containing CDS sequences
### `preappend_species_to_header.py`
Reads file name and preappends Genus_species identifiers to FASTA headers
### `fasta_to_oneline.py`
Converts multi-line FASTA sequences to single-line format
### `trim_header.py`
Trims FASTA headers to achieve a normalized >Genus_species_GeneID format
### `combine_gene_cds_directories.py`
Merges FASTA files from separate directories containing sequences from the same species
### `remove_gene_from_header.py`
Removes gene name from FASTA headers
## KIPEs Filtering
A collection of Python scripts that collect, concatenate, and filter the best gene hits identified by KIPEs
### `collect_best_gene_hits.py`
Collects and concatenates the best gene hits from each species identified by KIPEs
### `filter_best_gene_hits.py`
Filters and deduplicates gene hits based on conserved residue scores from the corresponding summary files
### `filter_outgroup_gene_hits.py`
Applies stricter filtering parameters for outgroup gene sequences
### `collect_cds_from_pep_alignment.py`
Retrieves CDS corresponding to peptide sequences used in an alignment using normalized headers
## iTOL KIPEs Annotation
A collection of Python scripts used for processing and preparing data for visualization in iTOL
### `extract_conserved_residues.py`
Extracts conserved residue scores from summary files and creates a compatible gradient annotation CSV format file
### `split_gene_conserved_residues.py`
Splits the combined conserved residue data file into separate files for each gene
## Presence-Absence Matrix
A collection of Python and R scripts used to prepare and create a presence-absence matrix with conserved residue values
### `extract_best_gene_hits.py`
Extracts the best gene hits for each species and creates a consolidated data file with corresponding conserved residue scores
### `create_conserved_residue_csv.py`
Converts the long-format data file into a CSV format matrix
### `presence_absence_matrix_plot.R`
Creates a presence-absence matrix with BUSCO completeness bars
