import React, { useState } from 'react';

function App() {
  const [subreddit, setSubreddit] = useState('');
  const [limit, setLimit] = useState(1000);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const response = await fetch('http://localhost:5000/scrape', {
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
    <div>
      <h2>Reddit Scraper</h2>
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
        <button type="submit" disabled={loading}>
          {loading ? 'Scraping...' : 'Scrape'}
        </button>
      </form>
    </div>
  );
}

export default App;