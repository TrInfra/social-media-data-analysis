#pip install textblob
#pip install nltk
import json
from pathlib import Path
import nltk
from textblob import TextBlob

dir = Path('./Data/Processed')

total_polarity = 0
total_subjectivity = 0
num_files = 0

for file in dir.iterdir():
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    text = data.get('lyrics', '')  

    blob = TextBlob(text)
    sentiment = blob.sentiment
    print(f"Arquivo: {file.name} - Polarity: {sentiment.polarity}, Subjectivity: {sentiment.subjectivity}")
    
    total_polarity += sentiment.polarity
    total_subjectivity += sentiment.subjectivity
    num_files += 1
    
if num_files > 0:
    avg_polarity = total_polarity / num_files
    avg_subjectivity = total_subjectivity / num_files
    print(f"\nMédia da Polaridade: {avg_polarity}, Média da Subjectividade: {avg_subjectivity}")
else:
    print("Nenhum arquivo JSON encontrado.")
    print("Fim do processamento.")
