import pandas as pd

file_path = "/home/abera/data1/data1/five_genes/willowTestData/GDRcalculationResultSJ/AberaTest__five_genes_distance_matrice_list__Population__gdr.tsv"
df = pd.read_csv(file_path, sep="\t")

super_pop_groups = {
    "AFR": ["AFR___ACB", "AFR___ASW", "AFR___ESN", "AFR___GWD", "AFR___LWK", "AFR___MSL", "AFR___YRI"],
    "AMR": ["AMR___CLM", "AMR___MXL", "AMR___PEL", "AMR___PUR"],
    "EAS": ["EAS___CDX", "EAS___CHB", "EAS___CHS", "EAS___JPT", "EAS___KHV"],
    "EUR": ["EUR___CEU", "EUR___FIN", "EUR___GBR", "EUR___IBS", "EUR___TSI"],
    "SAS": ["SAS___BEB", "SAS___GIH", "SAS___ITU", "SAS___PJL", "SAS___STU"]
}

df = df.dropna(axis=1, how="all")  
available_columns = df.columns.tolist()

super_pop_stats = {}
for super_pop, sub_pops in super_pop_groups.items():
    valid_columns = [col for col in sub_pops if col in available_columns]
    if valid_columns:
        super_pop_stats[super_pop] = {
            "min_gdr": df[valid_columns].min().min(),
            "max_gdr": df[valid_columns].max().max(),
        }

sub_pop_stats = {}
for sub_pop in available_columns[1:]:  
    if sub_pop in available_columns:
        sub_pop_stats[sub_pop] = {
            "min_gdr": df[sub_pop].min(),
            "max_gdr": df[sub_pop].max(),
        }

super_pop_df = pd.DataFrame.from_dict(super_pop_stats, orient="index")
sub_pop_df = pd.DataFrame.from_dict(sub_pop_stats, orient="index")

print("Super Population GDR Stats:")
print(super_pop_df)

print("\nSub Population GDR Stats:")
print(sub_pop_df)

super_pop_df.to_csv("/home/abera/data1/data1/five_genes/super_population_gdr_stats.tsv", sep="\t")
sub_pop_df.to_csv("/home/abera/data1/data1/five_genes/sub_population_gdr_stats.tsv", sep="\t")
