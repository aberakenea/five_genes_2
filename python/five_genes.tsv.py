import os
import pandas as pd
import re

dist_dir = "/home/abera/data1/data1/five_genes/distance_matrices"

# Mapping for population descriptions
population_mapping = {
    "AFR": "African",
    "EUR": "European",
    "EAS": "East Asian",
    "SAS": "South Asian",
    "AMR": "American"
}

group_description_mapping = {
    "AFR": "Africa",
    "EUR": "Europe",
    "EAS": "East Asia",
    "SAS": "South Asia",
    "AMR": "Americas"
}

all_samples = set()

# Read all samples from distance matrix files
for filename in os.listdir(dist_dir):
    if filename.endswith(".tsv"):
        file_path = os.path.join(dist_dir, filename)
        df = pd.read_csv(file_path, sep='\t', index_col=0)
        all_samples.update(df.index)

# Functions to extract population and group information
def infer_population(sample_id):
    match = re.match(r"([A-Z]{3}___[A-Z]{3})___", sample_id)
    return match.group(1) if match else "Unknown"

def infer_group_description(group_name):
    main_code = group_name.split("___")[0]
    sub_code = group_name.split("___")[1]
    main_description = group_description_mapping.get(main_code, "Unknown")
    return f"{main_description} from {sub_code}"

sample_data_rows = []
group_data_dict = {}

# Process each sample
for sample in sorted(all_samples):
    population = infer_population(sample)
    group_description = infer_group_description(population)

    # Append sample data
    sample_data_rows.append({"SampleID": sample, "Population": population})

    # Store unique groups
    if population not in group_data_dict:
        group_data_dict[population] = {
            "GroupCategory": "Population",
            "GroupName": population,
            "GroupDescription": group_description
        }

# Convert to DataFrames
sample_data = pd.DataFrame(sample_data_rows)
group_data = pd.DataFrame.from_dict(group_data_dict, orient="index")

# Save as TSV files
sample_data_path = os.path.join(dist_dir, "sample_data.tsv")
group_data_path = os.path.join(dist_dir, "group_data.tsv")

sample_data.to_csv(sample_data_path, sep='\t', index=False)
group_data.to_csv(group_data_path, sep='\t', index=False)

print(f"Files created:\n- {sample_data_path}\n- {group_data_path}")
