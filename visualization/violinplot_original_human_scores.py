import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# File paths for the databases
scores_db_path = '/home/jeff/PycharmProjects/llm-agent/webui/scores.db'  # Replace with your actual path
summaries_db_path = '/home/jeff/PycharmProjects/llm-agent/webui/GPT4_summaries.db'  # Replace with your actual path
# Establish connections to the databases
conn_scores = sqlite3.connect(scores_db_path)
conn_summaries = sqlite3.connect(summaries_db_path)

# Read the 'score' table from 'scores.db'
score_df = pd.read_sql_query("SELECT * FROM score;", conn_scores)

# Read the 'Summaries' table from 'GPT4_summaries.db'
summaries_df = pd.read_sql_query("SELECT * FROM Summaries;", conn_summaries)

# Joining the tables on 'summary_id' from score_df and 'id' from summaries_df
merged_df = pd.merge(left=score_df, right=summaries_df, how='left', left_on='summary_id', right_on='id')

# Creating adjusted score columns (replace with your actual adjustment logic)
adjusted_columns = {
    'accuracy_adjusted': merged_df['accuracy_y'] - 1,
    'relevance_adjusted': merged_df['relevance_y'] - 1,
    'creativity_adjusted': merged_df['novelty'] - 1,
    'specificity_adjusted': merged_df['specificity_y'] - 1,
    'feasibility_adjusted': merged_df['feasibility_y'] - 1
}
merged_df = merged_df.assign(**adjusted_columns)

# Melt the DataFrame for visualization, focusing on adjusted scores and 'model'
melted_merged_df = merged_df.melt(id_vars=["model"], value_vars=list(adjusted_columns.keys()), var_name="Metric", value_name="Score")

# Adjust the Metric column to remove "_adjusted" and capitalize
melted_merged_df['Metric'] = melted_merged_df['Metric'].str.replace('_adjusted', '').str.capitalize()

# Convert 'Score' to numeric
melted_merged_df['Score'] = pd.to_numeric(melted_merged_df['Score'], errors='coerce')

# Define color palette
merged_palette = sns.color_palette("hsv", len(merged_df['model'].unique()))

# Plotting the violin plot
plt.figure(figsize=(15, 8))
ax = sns.violinplot(x="Metric", y="Score", hue="model", data=melted_merged_df, palette=merged_palette, split=True)

# Customize plot elements
ax.set_xlabel("Metric Adjusted", fontsize=23, color='black', labelpad=20, fontweight='normal', fontname='DejaVu Sans')
ax.set_ylabel("Score", fontsize=23, color='black', labelpad=20, fontweight='normal', fontname='DejaVu Sans')
plt.legend(title="Model Name", bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()

# Close the database connections
conn_scores.close()
conn_summaries.close()