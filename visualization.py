import sqlite3
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Define the path to scores.db
scores_db_path = "/home/jeff/PycharmProjects/llm-agent/webui/scores.db"
gpt4_db_path = "/home/jeff/PycharmProjects/llm-agent/webui/GPT4_summaries.db"

# Fetch the data from scores.db
conn = sqlite3.connect(scores_db_path)
cursor = conn.cursor()
cursor.execute("SELECT summary_id, author, accuracy, relevance, creativity, specificity, feasibility FROM score")
scores_data = cursor.fetchall()
conn.close()

# Fetch the model names and task indices from GPT4_summaries.db
conn = sqlite3.connect(gpt4_db_path)
cursor = conn.cursor()
cursor.execute("SELECT id, model, task_index FROM Summaries")
gpt4_data = cursor.fetchall()
conn.close()

scores = [score[3] for score in scores_data if score[0] == 49]
print(scores)

# calculate the median score
median_score = np.median(scores)
print(median_score)