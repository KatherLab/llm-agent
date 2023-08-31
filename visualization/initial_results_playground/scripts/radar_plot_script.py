
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi

# Connect to SQLite database
conn = sqlite3.connect('GPT4_summaries.db')
cur = conn.cursor()

# Execute a query to retrieve relevant data from the 'Summaries' table
cur.execute("SELECT model, novelty, feasibility, correctness FROM Summaries;")
data = cur.fetchall()
conn.close()

# Convert the data into a DataFrame
df = pd.DataFrame(data, columns=['model', 'novelty', 'feasibility', 'correctness'])

# Calculate average scores for each model
average_scores = df.groupby('model').mean().reset_index()

# Convert scores into percentages
average_scores[['novelty', 'feasibility', 'correctness']] = average_scores[['novelty', 'feasibility', 'correctness']].apply(lambda x: (x / 10) * 100)

# Number of variables
num_vars = len(average_scores.columns[1:])

# Compute angle each axis in the plot will be located at
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

# The plot is a circle, so complete the loop
angles += angles[:1]

# Initialize the spider plot
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

# Helper function to plot each model's scores
def add_to_plot(data_row, color):
    values = data_row.values.flatten().tolist()
    values += values[:1] # repeat the first value to close the circular graph
    ax.fill(angles, values, color=color, alpha=0.25)
    ax.plot(angles, values, color=color, linewidth=2, label=data_row.name)

# Add each additional model's scores to the plot
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'b']
for i, row in average_scores.set_index('model').iterrows():
    add_to_plot(row, colors.pop(0))

# Polar axis labels
ax.set_thetagrids(np.degrees(angles[:-1]), average_scores.columns[1:])

# Go through labels and adjust alignment based on where it is in the circle
for label, angle in zip(ax.get_xticklabels(), angles):
    if angle in (0, np.pi):
        label.set_horizontalalignment('center')
    elif 0 < angle < np.pi:
        label.set_horizontalalignment('left')
    else:
        label.set_horizontalalignment('right')

# Y axis label
ax.set_rlabel_position(180 / num_vars)

# Add legend
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

# Add title
plt.title('Model Skill Scores', size=20, color='black', y=1.1)
plt.savefig('../radar_plot.png')
plt.show()
