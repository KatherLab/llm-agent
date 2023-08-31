
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to SQLite database
conn = sqlite3.connect('GPT4_summaries.db')
cur = conn.cursor()

# Execute a query to retrieve relevant data from the 'Summaries' table
cur.execute("SELECT model, novelty, feasibility, correctness, task_index FROM Summaries;")
data = cur.fetchall()
conn.close()

# Convert the data into a DataFrame
df = pd.DataFrame(data, columns=['model', 'novelty', 'feasibility', 'correctness', 'task'])

# Creating score plots according to each task
fig, axs = plt.subplots(3, 1, figsize=(15, 15))

for ax, column in zip(axs, ['novelty', 'feasibility', 'correctness']):
    for task in df['task'].unique():
        # Subset to the task
        subset = df[df['task'] == task]
        # Make a separate list for each task
        score_list = subset[column].values.tolist()
        # Also make a list of task labels which is as long as the task score list
        task_list = [task] * len(score_list)
        # Draw a scatterplot for each task's scores with a loop
        ax.scatter(task_list, score_list, alpha=0.5)
    ax.set_title(column)
    ax.set_xlabel('Task')
    ax.set_ylabel('Score')

plt.tight_layout()
plt.savefig('../score_plots.png')
plt.show()

