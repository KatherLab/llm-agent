
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# File paths
file_paths = [
    "csvs/1task.csv",
    "csvs/2task.csv",
    "csvs/3task.csv",
    "csvs/4task.csv",
    "csvs/5task.csv",
    "csvs/6task.csv",
    "csvs/7task.csv",
    "csvs/8task.csv",
    "csvs/9task.csv",
    "csvs/10task.csv"
]

# Adjusted columns to focus on
adjusted_columns = [
    "accuracy_adjusted",
    "relevance_adjusted",
    "creativity_adjusted",
    "specificity_adjusted",
    "feasibility_adjusted"
]

# Process and combine data using the 'model' column from each CSV
dataframes = []
for file_path in file_paths:
    df = pd.read_csv(file_path)[["model"] + adjusted_columns]
    # Model name adjustments
    model_renames = {
        "gpt-3.5-turbo": "gpt-3.5",
        "cot-gpt-4-zero-shot-cot": "cot-zero",
        "cot-gpt-4-manual-cot": "cot-manual",
        "llama-2-7b-chat": "llama2",
        "camel-gpt4": "camel",
        "babyagi-gpt-4": "babyagi"
    }
    df['model'] = df['model'].replace(model_renames)
    df.rename(columns={'model': 'Model'}, inplace=True)
    dataframes.append(df)

# Combine all data into a single DataFrame
combined_df = pd.concat(dataframes)

# Melt the DataFrame for easier plotting with seaborn
melted_df = combined_df.melt(id_vars=["Model"], var_name="Metric", value_name="Score")

# Adjust the Metric column to remove "_adjusted" and capitalize
melted_df['Metric'] = melted_df['Metric'].str.replace('_adjusted', '').str.capitalize()
full_palette = sns.color_palette("hsv", 31)  # Generate a palette with enough colors

c1 = full_palette[2]  # First color
cgpt4 = full_palette[4]  # First color
c2 = full_palette[5:10]  # Colors from index 10 to 13
c3 = full_palette[15]  # 21st color
c4 = full_palette[20]  # 31st color
c5 = full_palette[25]  # 31st color

# Merging colors for model groups
merged_palette = {
    "gpt-3.5": full_palette[2],  # Assigning c3 to gpt-3.5

    "gpt-4": full_palette[4],  # Assigning c1 to gpt-4
    "camel": full_palette[7],  # Assigning first color of c2 group
    "babyagi": full_palette[10],  # Assigning second color of c2 group
    "cot-zero": full_palette[13],  # Assigning third color of c2 group
    "cot-manual": full_palette[16],  # Assigning fourth color of c2 group
    "llama2": full_palette[23],  # Assigning c4 to llama2
    "bard": full_palette[30]  # Assigning c4 to bard
}
sns.set(style="whitegrid", font_scale=1.8)  # Increase font scale

# Define order of models
model_order = ["gpt-3.5", "gpt-4", "camel", "babyagi", "cot-zero", "cot-manual", "llama2", "bard"]

# Plotting the box plot
plt.figure(figsize=(15, 8))
ax = sns.boxplot(x="Metric", y="Score", hue="Model", data=melted_df, palette=merged_palette, hue_order=model_order)

# Customize plot elements
ax.set_xlabel("Metric Adjusted", fontsize=23, color='black', labelpad=20, fontweight='normal', fontname='Arial')
ax.set_ylabel("Score", fontsize=23, color='black', labelpad=20, fontweight='normal', fontname='Arial')
plt.legend(title="Model Name", bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()