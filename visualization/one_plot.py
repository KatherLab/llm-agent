import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# File paths for the databases
scores_db_path = '/home/jeff/PycharmProjects/llm-agent/webui/scores.db'
summaries_db_path = '/home/jeff/PycharmProjects/llm-agent/webui/GPT4_summaries.db'

# Establish connections to the databases
conn_scores = sqlite3.connect(scores_db_path)
conn_summaries = sqlite3.connect(summaries_db_path)

# Read the 'score' table from 'scores.db'
score_df = pd.read_sql_query("SELECT * FROM score;", conn_scores)

# Read the 'Summaries' table from 'GPT4_summaries.db'
summaries_df = pd.read_sql_query("SELECT * FROM Summaries;", conn_summaries)

# Joining the tables on 'summary_id' from score_df and 'id' from summaries_df
merged_df = pd.merge(left=score_df, right=summaries_df, how='left', left_on='summary_id', right_on='id')

# Model renaming
model_renames = {
    "gpt-3.5-turbo": "gpt-3.5",
    "cot-gpt-4-zero-shot-cot": "cot-zero",
    "cot-gpt-4-manual-cot": "cot-manual",
    "llama-2-7b-chat": "llama2",
    "camel-gpt4": "camel",
    "babyagi-gpt-4": "babyagi"
}
merged_df['model'] = merged_df['model'].replace(model_renames)

# Creating adjusted score columns
adjusted_columns = {
    'Accuracy': merged_df['accuracy_y'],
    'Relevance': merged_df['relevance_y'],
    'Creativity': merged_df['novelty'],
    'Specificity': merged_df['specificity_y'],
    'Feasibility': merged_df['feasibility_y']
}
merged_df = merged_df.assign(**adjusted_columns)

# Melt the DataFrame for visualization
melted_merged_df = merged_df.melt(id_vars=["model"], value_vars=list(adjusted_columns.keys()), var_name="Metric", value_name="Score")

# Convert 'Score' to numeric
melted_merged_df['Score'] = pd.to_numeric(melted_merged_df['Score'], errors='coerce')

# Define color palette
full_palette = sns.color_palette("hsv", 31)
merged_palette = {
    "gpt-3.5": full_palette[2],
    "gpt-4": full_palette[4],
    "camel": full_palette[7],
    "babyagi": full_palette[10],
    "cot-zero": full_palette[13],
    "cot-manual": full_palette[16],
    "llama2": full_palette[23],
    "bard": full_palette[30]
}
sns.set(style="whitegrid", font_scale=1.5)

# Define order of models
model_order = ["gpt-3.5", "gpt-4", "camel", "babyagi", "cot-zero", "cot-manual", "llama2", "bard"]

# Plotting the violin plot
plt.figure(figsize=(15, 8))
ax = sns.violinplot(x="Metric", y="Score", hue="model", data=melted_merged_df, palette=merged_palette, hue_order=model_order)

# Set the upper limit of the score to 10
ax.set_ylim(bottom=None)

# Customize plot elements
ax.set_xlabel("Metric original", fontsize=23, color='black', labelpad=20, fontweight='normal', fontname='DejaVu Sans')
ax.set_ylabel("Score", fontsize=23, color='black', labelpad=20, fontweight='normal', fontname='DejaVu Sans')
plt.legend(title="Model Name", bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()

# Close the database connections
conn_scores.close()
conn_summaries.close()