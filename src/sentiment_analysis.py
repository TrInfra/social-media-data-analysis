#pip install textblob
#pip install nltk
import json
from pathlib import Path
import nltk
from textblob import TextBlob

dir = Path('./Data/Processed')

num_files = 0
polarities = []
subjectivities = []

for file in dir.iterdir():
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    text = data.get('lyrics', '')  

    blob = TextBlob(text)
    sentiment = blob.sentiment
    print(f"File: {file.name} - Polarity: {sentiment.polarity}, Subjectivity: {sentiment.subjectivity}")
    
    polarities.append(sentiment.polarity)
    subjectivities.append(sentiment.subjectivity)
    num_files += 1

if num_files > 0:
    avg_polarity = sum(polarities) / num_files
    avg_subjectivity = sum(subjectivities) / num_files
    print(f"\nAverage Polarity: {avg_polarity}, Average Subjectivity: {avg_subjectivity}")
else:
    print("No JSON files found.")
    print("End of processing.")
