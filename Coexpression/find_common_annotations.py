#!/usr/bin/env python3

import os
import pandas as pd
from collections import Counter

def read_file(filepath):
    # Try reading with common delimiters and print info
    for sep in ["\t", ",", ";", " "]:
        try:
            df = pd.read_csv(filepath, sep=sep)
            if "FunctionalAnnotation" in df.columns:
                print(f"Read {os.path.basename(filepath)} successfully with separator '{sep}'")
                return df
        except Exception:
            continue
    print(f"Failed to read {filepath} with any common delimiter.")
    return None

def main():
    directory = "clade1"
    if not os.path.isdir(directory):
        print(f"Directory '{directory}' not found.")
        return

    annotation_counts = Counter()
    files_processed = 0

    for filename in os.listdir(directory):
        if filename.endswith((".csv", ".tsv", ".txt")):
            filepath = os.path.join(directory, filename)
            df = read_file(filepath)

            if df is None or "FunctionalAnnotation" not in df.columns:
                print(f"Skipping {filename}: could not read or missing 'FunctionalAnnotation' column.")
                continue

            top_50 = df.head(50)
            annotations = set(top_50["FunctionalAnnotation"].dropna().astype(str))

            # Count each unique annotation once per file
            for annotation in annotations:
                annotation_counts[annotation] += 1

            files_processed += 1

    if files_processed == 0:
        print("No files were successfully processed.")
        return

    # Filter annotations found in at least 2 files
    common_annotations = [ann for ann, count in annotation_counts.items() if count >= 2]

    print(f"\nFunctional annotations found in top 50 of at least 2 files ({len(common_annotations)} found):")
    for annotation in sorted(common_annotations):
        print(annotation)

    with open("common_annotations_at_least_two_files.txt", "w") as f:
        for annotation in sorted(common_annotations):
            f.write(annotation + "\n")
    print("\nSaved results to common_annotations_at_least_two_files.txt")

if __name__ == "__main__":
    main()
          
