import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load the data from the database into a DataFrame
conn = sqlite3.connect('/home/jeff/PycharmProjects/llm-agent/webui/GPT4_summaries.db')  # Adjust the path if necessary
query = "SELECT model, accuracy, relevance, novelty, specificity, feasibility FROM summaries"
df = pd.read_sql_query(query, conn)
conn.close()

# 2. Setup the visualization environment
sns.set_style("whitegrid")
plt.figure(figsize=(18, 12))

# 3. Generate swarm plots for each metric
metrics = df.columns[1:]
for i, metric in enumerate(metrics, 1):
    plt.subplot(2, 3, i)
    sns.violinplot(x="model", y=metric, data=df, palette="tab10",cut=0,inner="quartile", )#, min = 5, max = 10
    plt.title(metric.capitalize())
    plt.ylim(6, 10)

    plt.xticks(rotation=45, ha='right')

plt.suptitle("", y=1.05)
# add legend for models

# save as svg


plt.tight_layout()
plt.show()
plt.savefig(f"swarm_plot_by_model.svg")
