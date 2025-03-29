import os
import pandas as pd
from Bio import SeqIO
from Bio import AlignIO

# File paths
gdr_file = "/home/abera/data1/data1/five_genes/AberaTest__five_genes_distance_matrice_list__Population__gdr.tsv"
fasta_dir = "/home/abera/data1/data1/five_genes/5genes/uniq_aln.fa"
samplemap_dir = "/home/abera/data1/data1/five_genes/5genes/uniq_samplemap.tsv"
output_dir = "/home/abera/data1/data1/five_genes/mutation_results"
os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

# Load GDR values
gdr_df = pd.read_csv(gdr_file, sep="\t")

# Ensure the required column exists
if "SAS___BEB" not in gdr_df.columns or gdr_df.empty:
    raise ValueError("No valid GDR values found in the dataset.")

gdr_df = gdr_df[["gene name", "SAS___BEB"]].dropna()
lowest_gdr_gene = gdr_df.loc[gdr_df["SAS___BEB"].idxmin()]

gene_name = lowest_gdr_gene["gene name"]
gdr_value = lowest_gdr_gene["SAS___BEB"]
print(f"Gene with lowest GDR (SAS_BEB): {gene_name} ({gdr_value})")

# Find corresponding sample map file
matching_tsv_files = [f for f in os.listdir(samplemap_dir) if gene_name in f]
if not matching_tsv_files:
    raise FileNotFoundError(f"No sample map found for gene: {gene_name}")

tsv_file = os.path.join(samplemap_dir, matching_tsv_files[0])
print(f"Using sample map file: {tsv_file}")

# Load the sample map
df_sample_map = pd.read_csv(tsv_file, sep="\t", header=None, dtype=str)
sas_beb_samples = {}

# Extract samples that contain "SAS___BEB"
for index, row in df_sample_map.iterrows():
    sample_id = row[0]  # First column = sample name
    populations = row[1:].dropna()

    for pop_list in populations:
        pop_list = pop_list.split(",")  # Split multiple populations
        for pop in pop_list:
            pop = pop.strip()
            if "SAS___BEB" in pop:
                sas_beb_samples.setdefault(sample_id, []).append(pop)

# Find corresponding FASTA file
matching_fasta_files = [f for f in os.listdir(fasta_dir) if gene_name in f]
if not matching_fasta_files:
    raise FileNotFoundError(f"No FASTA sequence found for gene: {gene_name}")

fasta_file = os.path.join(fasta_dir, matching_fasta_files[0])
print(f"Using FASTA sequence file: {fasta_file}")

# Load the sequence alignment
alignment = AlignIO.read(fasta_file, "fasta")
if len(alignment) == 0:
    raise ValueError("FASTA file is empty or improperly formatted.")

# Use the first sequence as a reference
reference_seq = alignment[0].seq
reference_id = alignment[0].id
print(f"Reference sequence: {reference_id}")

# Find mutation positions
mutation_positions = {}
for record in alignment[1:]:  # Compare all sequences to the reference
    sample_id = record.id
    seq = record.seq
    mutations = []

    for i, (ref_base, sample_base) in enumerate(zip(reference_seq, seq)):
        if ref_base != sample_base and ref_base != "-" and sample_base != "-":
            mutations.append((i + 1, ref_base, sample_base))  # Position is 1-based

    if mutations:
        mutation_positions[sample_id] = mutations

# Save sample mapping results
sample_output_file = os.path.join(output_dir, f"{gene_name}_SAS_BEB_samples.tsv")
with open(sample_output_file, "w") as f:
    f.write(f"Gene with lowest GDR (SAS_BEB): {gene_name} ({gdr_value})\n")
    f.write(f"Using sample map file: {tsv_file}\n\n")

    if sas_beb_samples:
        f.write("Samples containing SAS___BEB:\n")
        for sample, populations in sas_beb_samples.items():
            f.write(f"{sample}: {', '.join(populations)}\n")
    else:
        f.write("No samples containing SAS___BEB found.\n")

print(f"Results saved: {sample_output_file}")

# Save mutation results
mutation_output_file = os.path.join(output_dir, f"{gene_name}_mutations.tsv")
with open(mutation_output_file, "w") as f:
    f.write(f"Gene with lowest GDR (SAS_BEB): {gene_name} ({gdr_value})\n")
    f.write(f"Using sample map file: {tsv_file}\n")
    f.write(f"Using FASTA sequence file: {fasta_file}\n")
    f.write(f"Reference sequence: {reference_id}\n\n")

    if mutation_positions:
        f.write("Mutations found:\n")
        for sample, mutations in mutation_positions.items():
            f.write(f"Sample {sample}:\n")
            for pos, ref, alt in mutations:
                f.write(f"  Position {pos}: {ref} → {alt}\n")
    else:
        f.write("No mutations detected.\n")

print(f"Mutation results saved to: {mutation_output_file}")
