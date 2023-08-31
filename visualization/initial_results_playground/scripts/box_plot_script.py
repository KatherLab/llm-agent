
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to SQLite database
conn = sqlite3.connect('GPT4_summaries.db')
cur = conn.cursor()

# Execute a query to retrieve relevant data from the 'Summaries' table
cur.execute("SELECT model, novelty, feasibility, correctness FROM Summaries;")
data = cur.fetchall()
conn.close()

# Convert the data into a DataFrame
df = pd.DataFrame(data, columns=['model', 'novelty', 'feasibility', 'correctness'])

# Create box plots
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

for ax, column in zip(axs, ['novelty', 'feasibility', 'correctness']):
    df.boxplot(column=column, by='model', ax=ax, grid=False, rot=90)
    ax.set_title(column)
    ax.set_xlabel('')

plt.suptitle('Box Plots of Model Skill Scores')
plt.savefig('../box_plots.png')
plt.show()
