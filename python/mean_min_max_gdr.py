import pandas as pd

file_path = "/home/abera/data1/data1/five_genes/willowTestData/GDRcalculationResultSJ/AberaTest__five_genes_distance_matrice_list__Population__gdr.tsv"
df = pd.read_csv(file_path, sep="\t")

df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')

super_pop_groups = {
    "AFR": ["AFR___ACB", "AFR___ASW", "AFR___ESN", "AFR___GWD", "AFR___LWK", "AFR___MSL", "AFR___YRI"],
    "AMR": ["AMR___CLM", "AMR___MXL", "AMR___PEL", "AMR___PUR"],
    "EAS": ["EAS___CDX", "EAS___CHB", "EAS___CHS", "EAS___JPT", "EAS___KHV"],
    "EUR": ["EUR___CEU", "EUR___FIN", "EUR___GBR", "EUR___IBS", "EUR___TSI"],
    "SAS": ["SAS___BEB", "SAS___GIH", "SAS___ITU", "SAS___PJL", "SAS___STU"]
}

super_pop_values = []
sub_pop_values = []

for sub_pop in df.columns[1:]:  
    valid_values = df[sub_pop].dropna().values  
    sub_pop_values.extend(valid_values)

for super_pop, sub_pops in super_pop_groups.items():
    valid_columns = [col for col in sub_pops if col in df.columns]

    if valid_columns:
        mean_super_values = df[valid_columns].mean(axis=1, skipna=True)
        super_pop_values.extend(mean_super_values.dropna().values)  

summary_stats = {
    "Population": ["Super", "Sub"],
    "Count": [len(super_pop_values), len(sub_pop_values)],
    "Mean GDR": [pd.Series(super_pop_values).mean(), pd.Series(sub_pop_values).mean()],
    "Min GDR": [pd.Series(super_pop_values).min(), pd.Series(sub_pop_values).min()],
    "Max GDR": [pd.Series(super_pop_values).max(), pd.Series(sub_pop_values).max()]
}

summary_df = pd.DataFrame(summary_stats)

print("\nSummary GDR Stats:")
print(summary_df)

summary_df.to_csv("/home/abera/data1/data1/five_genes/summary_gdr_stats.tsv", sep="\t", index=False)
