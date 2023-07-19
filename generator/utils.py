import subprocess
import openai
import pandas as pd
import os
def generate_evaluation(api_key,model, prompt, input_text):
    """
    Function to generate an evaluation of the input_text using the OpenAI API.

    Parameters:
    api_key (str): The OpenAI API key.
    model (str): The name of the model to use.
    prompt (str): The evaluation prompt.
    input_text (str): The text to evaluate.

    Returns:
    str: The evaluation of the input_text.
    """

    # Define the API request
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": input_text}
        ]
    )
    generated_text = response['choices'][0]['message']['content']

    return generated_text

