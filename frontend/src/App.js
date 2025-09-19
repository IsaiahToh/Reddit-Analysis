import React, { useState, useRef } from 'react';
import './App.css';

function App() {
  const [subreddit, setSubreddit] = useState('');
  const [postCount, setPostCount] = useState(1000);
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [error, setError] = useState('');
  const subredditInputRef = useRef(null);

  const handleScrape = async () => {
    if (!subreddit) {
      alert('Please enter a subreddit name');
      subredditInputRef.current.focus();
      return;
    }
    if (postCount < 1 || postCount > 1000) {
      alert('Post count must be between 1 and 1000');
      return;
    }
    setIsLoading(true);
    setError('');
    setResults([]);
    try {
      const response = await fetch('http://localhost:5000/api/scrape', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ subreddit, count: postCount }),
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to fetch posts');
      }
      const data = await response.json();
      setResults(data.posts || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  // Optional: focus input on mount
  React.useEffect(() => {
    subredditInputRef.current.focus();
  }, []);

  return (
    <div className="container">
      <h1>Reddit Scraper</h1>
      <div className="input-section">
        <div className="input-group">
          <label htmlFor="subredditInput">Subreddit</label>
          <input
            type="text"
            id="subredditInput"
            placeholder="Enter subreddit name"
            value={subreddit}
            onChange={e => setSubreddit(e.target.value)}
            ref={subredditInputRef}
            onKeyDown={e => { if (e.key === 'Enter' && !isLoading) handleScrape(); }}
          />
        </div>
        <div className="input-group">
          <label htmlFor="postCountInput">Post Count</label>
          <input
            type="number"
            id="postCountInput"
            value={postCount}
            min="1"
            max="1000"
            onChange={e => setPostCount(Number(e.target.value))}
          />
        </div>
        <button className="scrape-btn" onClick={handleScrape} disabled={isLoading}>
          {isLoading ? <span className="spinner"></span> : null}
          {isLoading ? 'Scraping...' : 'Scrape'}
        </button>
      </div>
      <div className="results-section">
        <div className="results-header">
          Results
        </div>
        <div className="results-content">
          {error && <div className="error">{error}</div>}
          {isLoading && <div className="loading">Fetching posts from Reddit...</div>}
          {!isLoading && results.length === 0 && !error && <div>No posts found.</div>}
          {results.map(post => (
            <div className="post-item" key={post.id}>
              <div className="post-title">{post.title}</div>
              <div className="post-meta">
                <span>👍 {post.score} points</span>
                <span>💬 {post.comments} comments</span>
                <span>👤 u/{post.author}</span>
                <span>📅 {new Date(post.created * 1000).toLocaleDateString()}</span>
              </div>
              <a href={post.url} target="_blank" rel="noopener noreferrer" className="post-link">
                View on Reddit →
              </a>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;