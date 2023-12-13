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
      // Fetching the data by calling the endpoint
      const response = await fetch(`/get-text-signature?hex=${encodeURIComponent(inputValue)}`);
      console.log(response)
      // Throwing error if the http call fails
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.text();
      console.log(result)
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
