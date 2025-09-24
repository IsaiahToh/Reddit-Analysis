import React, { useState } from 'react';
import './App.css';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

function App() {
  const [subreddit, setSubreddit] = useState('');
  const [limit, setLimit] = useState(500);
  const [loading, setLoading] = useState(false);

  //mew state for adding sentiment data 
  const[sentimentCounts, setSentimentCounts] = useState(null);

  //helper to load mock data from sentiment_data.json
  const loadMockData = async () => {
    const response = await fetch('/sentiment_data.json');
    const data = await response.json();

    const counts = { positive: 0, negative: 0, neutral: 0 };
    data.forEach(post => {
      if (post.sentiment === 1) counts.positive += 1;
      else if (post.sentiment === 0) counts.neutral += 1;
      else if (post.sentiment === -1) counts.negative += 1;
    });
    setSentimentCounts(counts);
  };



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

      // Load mock sentiment data after scraping
      await loadMockData();

    } else {
      alert('Error: ' + (await response.text()));
    }
    setLoading(false);
  };

  const testData = [
  { name: 'Positive', count: 10 },
  { name: 'Neutral', count: 5 },
  { name: 'Negative', count: 7 },
];

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

      {/* Show chart if sentimentCounts is available */}
        <div style={{ marginTop: '40px', width: '100%', height: 300 }}>
          <ResponsiveContainer>
            <BarChart data={testData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey='name'/>
              <YAxis/>
              <Tooltip/>
              <Legend/>
              <Bar dataKey='count' fill='#8884d8'/>
            </BarChart>
          </ResponsiveContainer>
        </div>
    </div>
  );
}

export default App;