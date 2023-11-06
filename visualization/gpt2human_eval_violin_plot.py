import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Connect to databases and load data
conn_summaries = sqlite3.connect('/path/to/GPT4_summaries.db')
summaries_data = pd.read_sql_query("SELECT * FROM Summaries", conn_summaries)

conn_scores = sqlite3.connect('/path/to/scores.db')
scores_data = pd.read_sql_query("SELECT * FROM score", conn_scores)

# Merge the two datasets on summary_id
merged_data = pd.merge(summaries_data, scores_data, left_on="id", right_on="summary_id", how="left")

# Prepare dataframe for the "relevance" category
df_relevance = merged_data[['model', 'relevance_x', 'relevance_y']].melt(id_vars='model', value_vars=['relevance_x', 'relevance_y'])
df_relevance.columns = ['Model', 'Source', 'Relevance']

# Plotting
plt.figure(figsize=(15, 8))
sns.violinplot(data=df_relevance, x="Model", y="Relevance", hue="Source", split=True, palette="pastel", inner="quartile", cut=0)
plt.title("Relevance Ratings by Model/llm-agent")
plt.ylabel("Relevance Score")
plt.xlabel("Model/llm-agent Name")
plt.xticks(rotation=45)
handles, _ = plt.gca().get_legend_handles_labels()
plt.legend(handles=handles[:2], title="Rating Source", labels=["GPT4 Ratings", "Human Expert Ratings"])
plt.tight_layout()
plt.show()
