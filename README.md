# akaike-1
# AI News Summarizer & Sentiment Analysis

## Overview
This application extracts news articles about a company, analyzes sentiment, identifies key topics, and converts the summary into Hindi speech. It also generates a comparative sentiment analysis plot.

## Features
- **News Extraction:** Fetches non-JS news articles using BeautifulSoup.  
- **Sentiment Analysis:** Analyzes article summaries using TextBlob.  
- **Topic Extraction:** Extracts key topics with NLTK.  
- **TTS Generation:** Converts summary to Hindi speech using gTTS.  
- **Comparative Analysis:** Generates sentiment plots using Matplotlib.

## Setup & Execution

### 1. Clone the Repository

git clone https://github.com/Divyateja2709/akaike-1.git
cd akaike-1
2. Create & Activate Virtual Environment

python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
3. Install Dependencies

pip install -r requirements.txt
4. Download Required NLTK Data
Run this in a Python shell:

python

import nltk
nltk.download('punkt')
nltk.download('stopwords')
5. Run the Application

python app.py
Access it at:


http://127.0.0.1:5000



