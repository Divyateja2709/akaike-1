from flask import Flask, request, jsonify, send_file
from utils.news_extraction import extract_news
from utils.sentiment_analysis import analyze_sentiments
from utils.tts_generation import generate_tts
from utils.comparative_analysis import plot_sentiments
import os

app = Flask(__name__)

# Create 'static' folder if it doesn't exist
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/api/news', methods=['GET'])
def get_news():
    company_name = request.args.get('company')
    if not company_name:
        return jsonify({"error": "Company name is required"}), 400
    
    articles = extract_news(company_name)
    return jsonify({"articles": articles})

@app.route('/api/sentiment', methods=['POST'])
def get_sentiments():
    data = request.json
    articles = data.get('articles', [])
    
    if not articles:
        return jsonify({"error": "No articles provided"}), 400
    
    sentiments = analyze_sentiments(articles)
    return jsonify({"sentiments": sentiments})

@app.route('/api/tts', methods=['POST'])
def generate_audio():
    data = request.json
    summary_text = data.get('summary', '')
    company_name = data.get('company_name', 'Company')
    
    if not summary_text:
        return jsonify({"error": "Summary text is required"}), 400
    
    audio_file_path = generate_tts(summary_text, company_name)
    
    if not os.path.exists(audio_file_path):
        return jsonify({"error": "Error generating TTS"}), 500
    
    return send_file(audio_file_path, as_attachment=True)

@app.route('/api/plot', methods=['POST'])
def generate_plot():
    data = request.json
    sentiments = data.get('sentiments', [])
    
    if not sentiments:
        return jsonify({"error": "Sentiment data is required"}), 400
    
    # Save the plot as an image and return the path
    plot_path = os.path.join('static', 'sentiment_plot.png')
    plot_sentiments(sentiments, plot_path)
    
    if not os.path.exists(plot_path):
        return jsonify({"error": "Error generating plot"}), 500
    
    return jsonify({"plot_path": f"/static/sentiment_plot.png"})

if __name__ == '__main__':
    app.run(debug=True)
