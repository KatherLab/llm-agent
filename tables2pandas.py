import re
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Create an empty DataFrame to store the results
results_df = pd.DataFrame(columns=['AGI', 'Task', 'GPT', 'Run', 'Table Index', 'Novelty', 'Feasibility', 'Correctness'])

for root_folder  in Path.cwd().glob('results_*'):

    # Loop through all the .md files in the root folder and its subfolders
    for file_path in root_folder.glob('**/*.md'):
        # if file_path.relative_to(root_folder.parent) != Path('results_babyagi/summaries/BabyAGI_A_gpt-4_0.md'):
        #     continue

        info = file_path.name.split('_')
        agi = info[0]
        task = info[1]
        if root_folder.name in ['results_chain-of-thought-davinci', 'results_vanilla-35']:
            gpt= 'gpt-3.5-turbo' if "vanilla" in root_folder.name else info[2].rsplit('-', 1)[0] 
            run = int(info[2].rsplit('-', 1)[1].split('.')[0])
        else:
            gpt = info[2]
            run = int(info[3].split('.')[0])

        # Open the file and read its contents
        with open(file_path, 'r') as file:
            file_contents = file.read()

        # Use regex to find all the tables in the file
        table_regex = r'## Summary table by gpt-4\n\|.*\|\n\|.*\|\n\|.*\|[\n\S\s]*?(?=##|\Z)'
        table_matches = re.findall(table_regex, file_contents)


        # Loop through each table and extract the desired numbers
        for i, table_match in enumerate(table_matches):
            table_lines = table_match.split('\n')
            novelty = int(table_lines[3].split('|')[4].strip())
            feasibility = int(table_lines[3].split('|')[5].strip())
            correctness = int(table_lines[3].split('|')[6].strip())

            
            # Add the results to the DataFrame
            results_df = pd.concat([results_df, pd.DataFrame({
                'AGI': [agi],
                'Task': [task],
                'GPT': [gpt],
                'Run': [run],
                'Table Index': [i],
                'Novelty': [novelty],
                'Feasibility': [feasibility],
                'Correctness': [correctness]
            })], ignore_index=True)



df = results_df.sort_values(by=['AGI', 'GPT', 'Task', 'Run', 'Table Index' ]).reset_index(drop=True)


df = df.drop_duplicates(subset=[col for col in df.columns if col != "Table Index"])
df.to_csv('summary.csv' , index=False)








# ----------------------------------- Evaluate Results -------------------------------------------------
df = df.groupby(['AGI', 'Task', 'GPT']).median().reset_index()
df['AGI_GPT'] = df['AGI']+'_'+df['GPT']



fondict = {'fontweight':'bold'}
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.size'] = 11


# Create a facet grid with one plot for each metric
fig, ax = plt.subplots(4, 3, figsize=(12, 12), sharex=True, sharey=True)
ax = iter(ax.flatten())

for n, (name, group) in enumerate(df.groupby("Task")):
    

    axis = next(ax)
    sns.barplot(group, y='AGI_GPT', x='Novelty',  ax=axis)
    axis.set_ylabel("Task"+name, fontdict=fondict) 
    axis.set_xlabel(axis.get_xlabel(), fontdict=fondict)  if n==3 else axis.set_xlabel('')
        

    axis = next(ax)
    # axis.set_title("Task"+name, fontdict=fondict)
    sns.barplot(group, y='AGI_GPT', x='Feasibility',  ax=axis)
    axis.set_ylabel('')
    axis.set_xlabel(axis.get_xlabel(), fontdict=fondict)  if n==3 else axis.set_xlabel('')

    axis = next(ax)
    sns.barplot(group, y='AGI_GPT', x='Correctness',  ax=axis)
    axis.set_ylabel('')
    axis.set_xlabel(axis.get_xlabel(), fontdict=fondict)  if n==3 else axis.set_xlabel('')


fig.tight_layout()
fig.savefig('results.png')