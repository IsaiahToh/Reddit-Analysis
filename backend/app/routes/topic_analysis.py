from flask import Blueprint, request, jsonify

topic_routes = Blueprint('topic_routes', __name__)

ERROR_NO_JSON = "No JSON data provided"
ERROR_NO_POSTS = "No posts provided"

from app.services.nmf_word2vec import extract_topics, extract_trending_lingo

@topic_routes.route('/api/analyze-topics', methods=['POST'])
def analyze_topics():
    """
    Analyze posts to extract topics and trending lingo
    
    Request body:
    {
        "posts": ["post1 text", "post2 text", ...],
        "n_topics": 5,           // optional, default varies by service
        "n_top_words": 10,       // optional
        "n_top_lingo": 10        // optional
    }
    
    Response:
    {
        "success": true,
        "topics": [["word1", "word2", ...], ...],
        "trending_lingo": ["slang1", "slang2", ...],
        "metadata": {
            "total_posts": 100,
            "topics_found": 5,
            "service_used": "nmf_word2vec"
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": ERROR_NO_JSON
            }), 400
        
        posts = data.get('posts', [])
        if not posts:
            return jsonify({
                "success": False,
                "error": ERROR_NO_POSTS
            }), 400
        
        n_topics = data.get('n_topics', 5)
        n_top_words = data.get('n_top_words', 10)
        n_top_lingo = data.get('n_top_lingo', 10)
        
        print(f"🔍 Analyzing {len(posts)} posts...")
        for i, post in enumerate(posts[:3]):
            print(f"Post {i+1}: {post[:100]}...")
        
        print("🎯 Extracting topics...")
        topics = extract_topics(posts, n_topics=n_topics, n_top_words=n_top_words)
        print(f"✅ Found {len(topics)} topics")
        
        print("🗣️ Extracting trending lingo...")
        trending_lingo = extract_trending_lingo(posts, n_top_lingo=n_top_lingo)
        print(f"✅ Found {len(trending_lingo)} lingo terms")
        
        response = {
            "success": True,
            "topics": topics,
            "trending_lingo": trending_lingo,
            "metadata": {
                "total_posts": len(posts),
                "topics_found": len(topics),
                "lingo_found": len(trending_lingo),
                "service_used": "nmf_word2vec",
                "parameters": {
                    "n_topics": n_topics,
                    "n_top_words": n_top_words,
                    "n_top_lingo": n_top_lingo
                }
            }
        }
        
        print("📊 Results:")
        print(f"Topics: {topics}")
        print(f"Lingo: {trending_lingo}")
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"❌ Error in analyze_topics: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Analysis failed: {str(e)}"
        }), 500

@topic_routes.route('/api/extract-topics-only', methods=['POST'])
def extract_topics_only():
    """
    Extract only topics (no lingo)
    
    Request body:
    {
        "posts": ["post1 text", "post2 text", ...],
        "n_topics": 5,           // optional
        "n_top_words": 10        // optional
    }
    """
    try:
        data = request.get_json()
        
        if not data or not data.get('posts'):
            return jsonify({
                "success": False,
                "error": ERROR_NO_POSTS
            }), 400
        
        posts = data['posts']
        n_topics = data.get('n_topics', 5)
        n_top_words = data.get('n_top_words', 10)
        
        print(f"🎯 Extracting topics from {len(posts)} posts...")
        topics = extract_topics(posts, n_topics=n_topics, n_top_words=n_top_words)
        
        return jsonify({
            "success": True,
            "topics": topics,
            "metadata": {
                "total_posts": len(posts),
                "topics_found": len(topics),
                "service_used": "nmf_word2vec"
            }
        }), 200
        
    except Exception as e:
        print(f"❌ Error in extract_topics_only: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Topic extraction failed: {str(e)}"
        }), 500

@topic_routes.route('/api/extract-lingo-only', methods=['POST'])
def extract_lingo_only():
    """
    Extract only trending lingo (no topics)
    
    Request body:
    {
        "posts": ["post1 text", "post2 text", ...],
        "n_top_lingo": 10        // optional
    }
    """
    try:
        data = request.get_json()
        
        if not data or not data.get('posts'):
            return jsonify({
                "success": False,
                "error": ERROR_NO_POSTS
            }), 400
        
        posts = data['posts']
        n_top_lingo = data.get('n_top_lingo', 10)
        
        print(f"🗣️ Extracting lingo from {len(posts)} posts...")
        trending_lingo = extract_trending_lingo(posts, n_top_lingo=n_top_lingo)
        
        return jsonify({
            "success": True,
            "trending_lingo": trending_lingo,
            "metadata": {
                "total_posts": len(posts),
                "lingo_found": len(trending_lingo),
                "service_used": "nmf_word2vec"
            }
        }), 200
        
    except Exception as e:
        print(f"❌ Error in extract_lingo_only: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Lingo extraction failed: {str(e)}"
        }), 500

@topic_routes.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "success": True,
        "message": "Topic analysis service is running",
        "service": "nmf_word2vec"
    }), 200