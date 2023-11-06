import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define the order of metrics
metric_order = ['Accuracy', 'Relevance', 'Creativity', 'Spec', 'Feas']

# Load the CSV files for GPT-4 and human expert scores
gpt4_scores = pd.read_csv('gpt4_scores.csv')
expert_scores = pd.read_csv('expert_scores.csv')

# Merge the dataframes based on the model column
merged_scores = pd.merge(gpt4_scores, expert_scores, on='Model', suffixes=('_gpt4', '_expert'))

# Create heatmaps for each metric
for metric in metric_order:
    # Calculate the difference between GPT-4 and expert scores
    merged_scores[metric] = merged_scores[f'{metric}_gpt4'] - merged_scores[f'{metric}_expert']

    # Sort the dataframe based on the order of models in the 'Accuracy' heatmap
    if metric == 'Accuracy':
        sorted_models = merged_scores[['Model', metric]].sort_values(by=metric)['Model']

    # Create a heatmap
    plt.figure(figsize=(12, 6))
    sns.heatmap(merged_scores.pivot('Model', metric, metric), annot=True, fmt=".2f", cmap="coolwarm")
    plt.title(f'{metric} Heatmap')

    # Save the heatmap as an image
    plt.savefig(f'{metric}_heatmap.png')

# Show the heatmaps
plt.show()