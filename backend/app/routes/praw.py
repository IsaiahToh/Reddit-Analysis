from flask import Blueprint, request, send_file
from app.services.praw import scrape_subreddit

praw_bp = Blueprint('praw_bp', __name__)

@praw_bp.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    subreddit = data.get('subreddit')
    if not subreddit:
        return {"error": "Please provide a subreddit."}, 400
    limit = int(data.get('limit', 1000))
    csv_path = scrape_subreddit(subreddit, limit)
    return send_file(csv_path, as_attachment=True)