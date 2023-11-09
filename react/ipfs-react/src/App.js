import React, { useState } from 'react';

function App() {
  const [inputValue, setInputValue] = useState(''); // State to hold the input value
  const [data, setData] = useState(null); // State to hold the API response data
  const [loading, setLoading] = useState(false); // State to handle the loading state

  // Handler for input change
  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  // Handler for button click to make the HTTP call
  const fetchData = async () => {
    setLoading(true);
    setData(null); // Clear the existing data
    try {
      const response = await fetch(`https://signature-compass-63lof.ondigitalocean.app/get-text-signature?hex=${encodeURIComponent(inputValue)}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();
      console.log()
      setData(result); // Set the data in state
    } catch (error) {
      console.error("Fetching data failed", error);
      setData({ error: error.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        placeholder="Enter your query of a signature in hex format"
      />
      <button onClick={fetchData} disabled={loading}>
        {loading ? 'Loading...' : 'Fetch Data'}
      </button>
      {data && (
        <div>
          <h2>Results:</h2>
          {/* Render your results here */}
          <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
