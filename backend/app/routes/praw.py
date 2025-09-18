from flask import Flask, request, jsonify, send_file
from app.services.praw import scrape_subreddit

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    subreddit = data.get('subreddit', 'passive_income')
    limit = int(data.get('limit', 1000))
    csv_path = scrape_subreddit(subreddit, limit)
    return send_file(csv_path, as_attachment=True)
