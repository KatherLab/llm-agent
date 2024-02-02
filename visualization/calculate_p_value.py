# Reading the merged file to perform the t-test
file_path = '/mnt/data/merged_tasks.csv'
merged_data = pd.read_csv(file_path)

# Focusing on the columns of interest: models, adjusted scores, and task_index
columns_of_interest = [
    'model',
    'task_index',
    'accuracy_adjusted',
    'relevance_adjusted',
    'creativity_adjusted',
    'specificity_adjusted',
    'feasibility_adjusted'
]
data = merged_data[columns_of_interest]

# Performing t-tests
# First, we need to identify the unique models to compare
unique_models = data['model'].unique()

# For each pair of models, perform a t-test for each adjusted score
from scipy.stats import ttest_ind
import itertools

# Create a dictionary to hold the p-values for each test
p_values = {score: {} for score in columns_of_interest[2:]}

# Perform t-test for each pair of models and each adjusted score
for score in columns_of_interest[2:]:
    for model1, model2 in itertools.combinations(unique_models, 2):
        # Filter data for each model
        data_model1 = data[data['model'] == model1][score]
        data_model2 = data[data['model'] == model2][score]

        # Perform t-test
        t_stat, p_val = ttest_ind(data_model1, data_model2, equal_var=False)

        # Save p-value
        p_values[score][(model1, model2)] = p_val

p_values