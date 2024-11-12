from data_collection import main as data_collection_main
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def create_sentiment_graph(artist, track_names, polarities_dict):
    ordered_polarities = [polarities_dict[track] for track in track_names]
    
    df = pd.DataFrame({
        'Music': track_names,
        'Polarity': ordered_polarities 
    })
    
    # Sort by polarity
    df = df.sort_values('Polarity', ascending=True)
    
    # Create the graph
    plt.figure(figsize=(12, 6))
    bars = plt.barh(df['Music'], df['Polarity'])
    
    # Customize the graph
    plt.title(f'Sentiment Analysis of {artist} Songs')
    plt.xlabel('Polarity (-1 = Sad, 0 = Neutral, 1 = Happy)')
    plt.ylabel('Songs')
    
    # Add lines for each sentiment level
    plt.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
    plt.axvline(x=-0.5, color='red', linestyle='--', alpha=0.3)
    plt.axvline(x=0.5, color='green', linestyle='--', alpha=0.3)
    
    # Add colors based on polarity
    for i, bar in enumerate(bars):
        if df['Polarity'].iloc[i] < -0.01:
            bar.set_color('red')
        elif df['Polarity'].iloc[i] > 0.2:
            bar.set_color('green')
        else:
            bar.set_color('gray')
    
    # Add polarity values on bars
    for i, v in enumerate(df['Polarity']):
        plt.text(v, i, f' {v:.2f}', va='center')
    
    # Adjust layout
    plt.tight_layout()
    
    # Add legend
    plt.figtext(0.02, 0.02, 'Red = Sad | Gray = Neutral | Green = Happy', 
                fontsize=8, ha='left')
    
    plt.show()
if __name__ == "__main__":
    ARTIST_NAME, track_names = data_collection_main()
    from sentiment_analysis import polarities
    create_sentiment_graph(ARTIST_NAME, track_names, polarities)