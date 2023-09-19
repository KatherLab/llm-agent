import seaborn as sns
# Extracting data for task1
import pandas as pd
from matplotlib import pyplot as plt
adjusted_columns = ['accuracy_adjusted', 'relevance_adjusted', 'creativity_adjusted', 'specificity_adjusted', 'feasibility_adjusted', 'red_flags_adjusted']
original_columns = ['accuracy', 'relevance', 'creativity', 'specificity', 'feasibility', 'red_flags']
# Identify all unique models from all tasks
all_models = pd.concat([pd.read_csv(f"{index}task.csv")['model'] for index in range(1, 11)]).unique()

# Create a fixed color palette based on the unique models
model_palette = dict(zip(all_models, sns.color_palette("tab10", len(all_models))))

'''
# Modified code to plot swarm plots with fixed colors for each model
for index in range(1, 11):
    task_df = pd.read_csv(f"{index}task.csv")
    model_order = sorted(task_df['model'].unique())
    # Swarm plot with rating categories as columns and models differentiated by color
    plt.figure(figsize=(15, 8))
    sns.swarmplot(
        data=task_df.melt(id_vars=['model', 'author'], value_vars=adjusted_columns, var_name='Rating Category',
                          value_name='Adjusted Score'),
        x='Rating Category', y='Adjusted Score', hue='model', size=6, palette=model_palette, dodge=True, hue_order=model_order)
    plt.title(f'Swarm Plot for Task{index} - Adjusted Scores by Rating Category')
    plt.xticks(rotation=45)
    plt.legend(title='Model Name', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig(f"swarm_adjusted_score/{index}task_swarm_adjusted_score.svg")
    plt.show()
'''
'''
# plot the box plot putting all the tasks together
for index in range(1, 11):
    task_df = pd.read_csv(f"{index}task.csv")
    model_order = sorted(task_df['model'].unique())
    # Swarm plot with rating categories as columns and models differentiated by color
    plt.figure(figsize=(15, 8))
    sns.boxplot(
        data=task_df.melt(id_vars=['model', 'author'], value_vars=adjusted_columns, var_name='Rating Category',
                          value_name='Adjusted Score'),
        x='Rating Category', y='Adjusted Score', hue='model', palette=model_palette, hue_order=model_order)
    plt.title(f'Box Plot for Task{index} - Adjusted Scores by Rating Category')
    plt.xticks(rotation=45)
    plt.legend(title='Model Name', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig(f"box_adjusted_score/{index}task_box_adjusted_score.svg")
    plt.show()
'''
# plot a box plot putting all the data from 10 tasks together
merged_df = pd.concat([pd.read_csv(f"{index}task.csv") for index in range(1, 11)])
model_order = sorted(merged_df['model'].unique())
plt.figure(figsize=(15, 8))
sns.boxplot(
    data=merged_df.melt(id_vars=['model', 'author'], value_vars=adjusted_columns, var_name='Rating Category',
                      value_name='Adjusted Score'),
    x='Rating Category', y='Adjusted Score', hue='model', palette=model_palette, hue_order=model_order)
plt.title(f'Box Plot for All Tasks - Adjusted Scores by Rating Category')
plt.xticks(rotation=45)
plt.legend(title='Model Name', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.savefig(f"box_adjusted_score/all_task_box_adjusted_score.svg")
plt.show()

# plot a box plot putting all the data from 10 tasks together with original scores
plt.figure(figsize=(15, 8))
sns.boxplot(
    data=merged_df.melt(id_vars=['model', 'author'], value_vars=original_columns, var_name='Rating Category',
                      value_name='Adjusted Score'),
    x='Rating Category', y='Adjusted Score', hue='model', palette=model_palette, hue_order=model_order)
plt.title(f'Box Plot for All Tasks - Original Scores by Rating Category')
plt.xticks(rotation=45)
plt.legend(title='Model Name', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.savefig(f"box_adjusted_score/all_task_box_original_score.svg")
plt.show()