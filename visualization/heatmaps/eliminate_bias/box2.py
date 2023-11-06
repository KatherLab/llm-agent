import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# List of original score columns and their corresponding adjusted columns
score_columns = ['accuracy', 'relevance', 'creativity', 'specificity', 'feasibility', 'red_flags']
adjusted_columns = ['accuracy_adjusted', 'relevance_adjusted', 'creativity_adjusted', 'specificity_adjusted', 'feasibility_adjusted', 'red_flags_adjusted']
extracted_files = ['1task.csv', '2task.csv', '3task.csv', '4task.csv', '5task.csv', '6task.csv', '7task.csv', '8task.csv', '9task.csv', '10task.csv']
csv_files = [file for file in extracted_files if file.endswith('.csv')]

all_tasks_df = pd.concat([pd.read_csv(f"{file}") for file in csv_files], ignore_index=True)
# Calculating the average adjusted scores for each model based on the 'model' column
model_avg_scores = (all_tasks_df.groupby('model')[adjusted_columns]).mean()



# Plotting the average adjusted scores for each model
plt.figure(figsize=(15, 10))
model_avg_scores.plot(kind='box', ax=plt.gca(), colormap='tab10')
plt.title('Average Original Scores for Each LLM Model')
plt.ylabel('Adjusted Score')
plt.xlabel('Model Name')
plt.legend(title='Rating Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
