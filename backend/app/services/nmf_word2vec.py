
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.cluster import KMeans
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
from collections import Counter
import numpy as np

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text) # remove URLs
    text = re.sub(r"[^a-z\s]", "", text) # remove punctuation/numbers
    text = re.sub(r"\s+", " ", text).strip() # remove extra spaces
    return text

# Extract topics using NMF
def extract_topics(posts, n_topics=5, n_top_words=10):
    cleaned_posts = [clean_text(post) for post in posts]

    # TF-IDF vectorization
    tfidf_vectorizer = TfidfVectorizer(max_df=0.9, min_df=2, stop_words='english')
    X_tfidf = tfidf_vectorizer.fit_transform(cleaned_posts)

    # Fit NMF
    nmf = NMF(n_components=n_topics, random_state=42)
    nmf_features = nmf.fit_transform(X_tfidf)
    feature_names = tfidf_vectorizer.get_feature_names_out()
    topics = []
    # Display top words for each topic
    for topic_idx, topic in enumerate(nmf.components_):
        top_words = [feature_names[i] for i in topic.argsort()[-n_top_words:][::-1]]
        topics.append(top_words)
    return topics

# Extract trending lingo/phrases using Word2Vec and KMeans clustering
def extract_trending_lingo(posts, n_clusters=None, n_top_lingo=5):
    cleaned_posts = [clean_text(post) for post in posts]
    tokenized_posts = [simple_preprocess(post) for post in cleaned_posts]
    w2v_model = Word2Vec(
        sentences=tokenized_posts,
        vector_size=100,
        window=5,
        min_count=1,
        workers=4,
        sg=1
    )

    # Extract all word vectors
    words = list(w2v_model.wv.index_to_key)
    word_vectors = np.array([w2v_model.wv[word] for word in words])
    if n_clusters is None:
        n_clusters = max(2, int(np.sqrt(len(words))))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(word_vectors)
    labels = kmeans.labels_
    # Map words to clusters
    cluster_to_words = {}
    for word, label in zip(words, labels):
        cluster_to_words.setdefault(label, []).append(word)

    # Per cluster, rank words by frequency in posts
    token_flat = [word for sentence in tokenized_posts for word in sentence]
    word_counts = Counter(token_flat)
    trending_lingo = []
    for cluster_words in cluster_to_words.values():
        sorted_words = sorted(cluster_words, key=lambda w: word_counts[w], reverse=True)
        trending_lingo.extend(sorted_words[:n_top_lingo]) # default 5 most frequent per cluster
    
    # Remove duplicates and show trending lingo
    trending_lingo = list(dict.fromkeys(trending_lingo))
    return trending_lingo

# Example usage for testing
if __name__ == "__main__":
    scraped_posts = sample_posts = [
    "Anyone else trying out the new ChatGPT update? The responses feel way smoother ngl.",
    "Bro this AI coding assistant is cracked, wrote my whole Python function in seconds.",
    "Lowkey worried about AI taking over jobs tho… automation vibes everywhere.",
    "Man Elden Ring DLC is brutal af, bosses keep one-shotting me lol.",
    "Valorant patch dropped today, Sage wall feels nerfed again 😭.",
    "Anyone grinding ranked in League? Solo queue is actual pain rn.",
    "Crypto market pumping today, ETH breaking resistance finally 🚀.",
    "Bruh Tesla stock tanked after earnings, investors mad salty.",
    "Anyone else dollar cost averaging into SPY? Feels like free money long-term.",
    "New season of Stranger Things dropped!! The nostalgia hits so hard.",
    "Honestly the writing feels mid, but the soundtrack is straight fire 🔥.",
    "Binge-watched in one night… sleep schedule = ruined lol.",
    "The new iPhone camera is insane, lowlight shots look professional.",
    "Why does every tech YouTuber keep hyping the same gadgets smh.",
    "Amazon delivery late AGAIN, kinda done with Prime tbh.",
    "Just finished Cyberpunk 2077 Phantom Liberty—fr tho, story >>> gameplay.",
    "Memecoins exploding rn, literally dog-themed tokens everywhere 😂.",
    "Twitter feels dead since the last update, barely any engagement.",
    "Netflix raising prices AGAIN, do they want me to pirate?",
    "PC building costs are wild, GPUs still overpriced as hell."
]
    topics = extract_topics(scraped_posts)
    print("Extracted Topics:")
    for idx, topic_words in enumerate(topics):
        print(f"Topic {idx + 1}: {', '.join(topic_words)}")
    trending_lingo = extract_trending_lingo(scraped_posts)
    print("Top Trending Lingo / Phrases:")
    print(", ".join(trending_lingo))
