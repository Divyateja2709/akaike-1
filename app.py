import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from utils.news_extraction import extract_news
from utils.sentiment_analysis import analyze_sentiments
from utils.tts_generation import generate_tts
from utils.comparative_analysis import plot_sentiments

app = Flask(__name__)

# Create 'static' folder if it doesn't exist
if not os.path.exists('static'):
    os.makedirs('static')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        company_name = request.form['company'].strip()

        # Validate input
        if not company_name:
            return render_template('index.html', error="Please enter a valid company name.")

        # Extract news articles
        articles = extract_news(company_name)

        # Handle case where no articles are found
        if not articles:
            return render_template('index.html', error=f"No news articles found for '{company_name}'.")

        # Perform sentiment analysis
        sentiments = analyze_sentiments(articles)

        # Generate a summary for TTS
        summary_text = " ".join([article['summary'] for article in articles if article['summary']])

        # Generate TTS and get the audio file path
        audio_file_path = generate_tts(summary_text, company_name)

        # Generate comparative analysis plot and save it to static folder
        plot_path = os.path.join('static', f"{company_name}_plot.png")
        plot_sentiments(sentiments, plot_path)

        return render_template(
            'results.html',
            sentiments=sentiments,
            audio_file_path=f"/{audio_file_path}",
            plot_path=f"/{plot_path}"
        )

    return render_template('index.html')


# API Endpoints
@app.route('/api/articles/<company_name>', methods=['GET'])
def get_articles(company_name):
    articles = extract_news(company_name)
    if not articles:
        return jsonify({"error": f"No news articles found for '{company_name}'"}), 404
    return jsonify({"articles": articles})


@app.route('/api/sentiments/<company_name>', methods=['GET'])
def get_sentiments(company_name):
    articles = extract_news(company_name)
    if not articles:
        return jsonify({"error": f"No news articles found for '{company_name}'"}), 404
    
    sentiments = analyze_sentiments(articles)
    return jsonify({"sentiments": sentiments})


@app.route('/api/tts/<company_name>', methods=['GET'])
def get_tts(company_name):
    articles = extract_news(company_name)
    summary_text = " ".join([article['summary'] for article in articles if article['summary']])
    
    if not summary_text:
        return jsonify({"error": "No valid content for TTS."}), 400
    
    audio_file_path = generate_tts(summary_text, company_name)
    return send_from_directory('static', os.path.basename(audio_file_path))


@app.route('/api/plot/<company_name>', methods=['GET'])
def get_plot(company_name):
    articles = extract_news(company_name)
    if not articles:
        return jsonify({"error": f"No articles found for '{company_name}'"}), 404

    sentiments = analyze_sentiments(articles)
    plot_path = os.path.join('static', f"{company_name}_plot.png")
    plot_sentiments(sentiments, plot_path)

    return send_from_directory('static', f"{company_name}_plot.png")


if __name__ == '__main__':
    app.run(debug=True)
