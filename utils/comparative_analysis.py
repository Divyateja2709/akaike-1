import matplotlib.pyplot as plt
import os

def plot_sentiments(sentiments, company_name):
    categories = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for result in sentiments:
        categories[result['sentiment']] += 1
    
    labels = list(categories.keys())
    values = list(categories.values())
    
    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color=['green', 'blue', 'red'])
    plt.title(f"Sentiment Analysis Comparison for {company_name}")
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Articles")
    
    # Define path to save the plot
    sanitized_name = "".join(c if c.isalnum() or c == "_" else "_" for c in company_name.strip().replace(" ", "_"))
    plot_path = os.path.join("static", f"{sanitized_name}_sentiment_plot.png")
    
    # Save the plot instead of showing it
    plt.savefig(plot_path)
    plt.close()  # Close the figure to avoid memory leaks
    
    print(f"Sentiment plot saved as {plot_path}")
    return plot_path
