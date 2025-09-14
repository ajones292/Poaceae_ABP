import os
import shutil

src_dir = "/vol/data/Final_Dataset/KIPEs/baits_cds/"
dst_dir = "/vol/data/Final_Dataset/KIPEs/cds/"

os.makedirs(dst_dir, exist_ok=True)

for filename in os.listdir(src_dir):
    if not filename.endswith(".cds.fasta"):
        continue

    src_path = os.path.join(src_dir, filename)
    dst_path = os.path.join(dst_dir, filename)

    if os.path.exists(dst_path):
        # Read both files and prepend
        with open(src_path, "r") as src, open(dst_path, "r") as dst:
            new_content = src.read() + dst.read()
        with open(dst_path, "w") as out:
            out.write(new_content)
    else:
        shutil.copy2(src_path, dst_path)  # copy with metadata