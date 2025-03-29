import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

np.random.seed(42)
super_gdr = np.random.normal(loc=0.7, scale=0.1, size=25)
sub_gdr = np.random.normal(loc=0.7, scale=0.1, size=130)

super_gdr = np.clip(super_gdr, 0.2, 1.1)
sub_gdr = np.clip(sub_gdr, 0.2, 1.1)

df = pd.DataFrame({
    'GDR': np.concatenate([super_gdr, sub_gdr]),
    'level': ['super'] * len(super_gdr) + ['sub'] * len(sub_gdr)
})

sns.set_style("whitegrid")
plt.figure(figsize=(8, 5))

colors = {"super": "orange", "sub": "green"}
sns.kdeplot(data=df, x="GDR", hue="level", fill=True, common_norm=False, palette=colors)

plt.xlabel("GDR", fontsize=12)
plt.ylabel("Density", fontsize=12)
plt.xticks([0.2, 0.7, 1.1], labels=["0.2", "0.7", "1.1"], fontsize=10)  # Set X-axis ticks
plt.yticks(np.arange(0, 10, 2), fontsize=10)  # Set y-axis ticks

legend_patches = [
    mpatches.Patch(color="green", label="sub"),
    mpatches.Patch(color="orange", label="super")
]
plt.legend(handles=legend_patches, title="level", title_fontsize=12, fontsize=10, loc="upper right", frameon=True)

output_path = "/home/abera/data1/data1/five_genes/gdr_density_plot.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.show()
print(f"Density plot saved at: {output_path}")
