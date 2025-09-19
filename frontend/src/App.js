import React, { useState } from 'react';
import './App.css';

function App() {
  const [subreddit, setSubreddit] = useState('');
  const [limit, setLimit] = useState(500);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const response = await fetch('http://localhost:5001/scrape', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ subreddit, limit }),
    });
    if (response.ok) {
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${subreddit}_posts_with_comments.csv`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      console.log('Scraping and download complete!');
    } else {
      alert('Error: ' + (await response.text()));
    }
    setLoading(false);
  };

  return (
    <div className='App'>
      <h1 className='gradient-header'>Reddit Scraper</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Subreddit"
          value={subreddit}
          onChange={e => setSubreddit(e.target.value)}
          required
        />
        <input
          type="number"
          placeholder="Limit"
          value={limit}
          onChange={e => setLimit(e.target.value)}
          min={1}
        />
        <button type="submit" className="scrape-btn" disabled={loading}>
          {loading ? 'Scraping...' : 'Scrape'}
        </button>
      </form>
    </div>
  );
}

export default App;