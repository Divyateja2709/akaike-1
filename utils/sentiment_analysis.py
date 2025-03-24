import nltk
from textblob import TextBlob
from nltk.corpus import stopwords
from collections import Counter
import string

# Download stopwords if not already present
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def extract_topics(text, top_n=5):
    words = nltk.word_tokenize(text.lower())  # Tokenize and convert to lowercase
    words = [word for word in words if word.isalnum() and word not in stop_words and word not in string.punctuation]
    word_freq = Counter(words)
    
    # Get the most common words as topics
    topics = [word for word, freq in word_freq.most_common(top_n)]
    return topics

def analyze_sentiments(articles):
    sentiment_results = []
    for article in articles:
        text = article['summary']
        
        # Sentiment Analysis
        sentiment = TextBlob(text).sentiment.polarity
        sentiment_label = "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
        
        # Topic Extraction
        topics = extract_topics(text)
        
        # Add sentiment and topics to results
        sentiment_results.append({
            "title": article['title'],
            "sentiment": sentiment_label,
            "topics": topics,
            "link": article['link']
        })
    
    return sentiment_results
