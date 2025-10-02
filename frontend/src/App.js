// frontend/src/App.js
import React, { useState } from 'react';
import './App.css';

function App() {
  const [inputText, setInputText] = useState('');
  const [analyzedText, setAnalyzedText] = useState('');
  const [summary, setSummary] = useState('');
  const [action, setAction] = useState('');
  const [confidence, setConfidence] = useState('');
  const [severity, setSeverity] = useState(''); // NEW: State for severity level
  const [isLoading, setIsLoading] = useState(false);

  const handleAnalyzeClick = async () => {
    setIsLoading(true);
    setAnalyzedText(inputText);
    setSummary('');
    setAction('');
    setConfidence('');
    setSeverity(''); // NEW: Clear old severity

    try {
      const response = await fetch('http://127.0.0.1:5000/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: inputText }),
      });
      const data = await response.json();
      setSummary(data.summary);
      setAction(data.recommended_action);
      setConfidence(data.confidence || 'N/A');
      setSeverity(data.severity || 'Low'); // NEW: Set severity from backend response
    } catch (error) {
      console.error("Error fetching AI response:", error);
      setSummary("Error: Could not connect to the analysis service.");
      setAction("Please check if the backend server is running.");
      setSeverity('High'); // NEW: Set severity to High on error
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <header>
        {/* Header is unchanged */}
        <div className="logo-section">
          <span className="logo-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="currentColor" viewBox="0 0 16 16"><path d="M4.771 2.373A6.002 6.002 0 0 1 12 8c0 1.57-.457 3.033-1.237 4.256-1.579 2.446-3.791 2.529-4.557 2.531l-.226.002-.016.001-.004.001-.002.001L4.292 15h-.25c-.114 0-.17-.01-.258-.016a.956.956 0 0 1-.168-.052 1.35 1.35 0 0 1-.104-.055 1.402 1.402 0 0 1-.16.14.773.773 0 0 1-.095.074c-.039.026-.073.047-.1.066-.02.012-.036.022-.047.028a.178.178 0 0 1-.059.014c-.027.004-.044.006-.053.006H3.32a.112.112 0 0 1-.06-.013c-.028-.009-.044-.019-.053-.027-.035-.03-.07-.06-.106-.092-.04-.035-.07-.06-.095-.074-.029-.02-.054-.037-.067-.046-.036-.026-.062-.042-.075-.05A1.36 1.36 0 0 1 2.453 14h-.25c-.477 0-.918-.088-1.259-.26C.81 13.562.628 13.178.5 12.753A6.002 6.002 0 0 1 4.771 2.373Zm-.021-.001C.635 3.593 0 5.768 0 8c0 2.232.635 4.407 1.75 6.001A7 7 0 0 0 4.292 15h.25a.25.25 0 0 0 .006-.001c-.015-.002-.029-.004-.042-.007a.955.955 0 0 0-.083-.026 1.378 1.378 0 0 0-.048-.015c-.067-.024-.12-.043-.153-.058-.04-.017-.064-.028-.078-.035-.022-.01-.035-.015-.042-.018-.011-.004-.017-.006-.019-.006H4.292a.25.25 0 0 0-.006.001c.015.002.029.004.042.007a.955.955 0 0 0 .083.026 1.378 1.378 0 0 0 .048-.015c.067-.024.12-.043-.153-.058.04-.017-.064-.028-.078-.035.022-.01.035-.015.042-.018.011-.004.017-.006.019-.006h.226c.767 0 2.978-.084 4.557-2.53A7 7 0 0 0 13 8c0-2.232-.635-4.407-1.75-6.001A7 7 0 0 0 4.75 2.372Z"/></svg>
          </span>
          <h1 className="title">SentinelMate</h1>
        </div>
        <p className="subtitle">AI Cybersecurity Co-Pilot & ScamShield</p>
      </header>

      <main>
        {/* Input section is unchanged */}
        <div className="section">
          <h2 className="section-title">Input Section</h2>
          <p className="section-description">Paste your server logs or a suspicious SMS/WhatsApp message below.</p>
          <textarea className="input-textarea" rows="8" placeholder="e.g., Failed SSH login for user root from 203.0.113.25..." value={inputText} onChange={(e) => setInputText(e.target.value)}/>
          <button className="analyze-button" onClick={handleAnalyzeClick} disabled={isLoading}>
            {isLoading ? 'Analyzing Text...' : 'Analyze Text'}
          </button>
        </div>

        {/* MODIFIED: The output card will now change its class based on severity */}
        <div className="section output-section">
          <h2 className="section-title">AI Interpretation</h2>
          <div className={`output-card severity-${severity.toLowerCase()}`}>
            {isLoading ? (
              <p className="loading-message">Loading AI Analysis...</p>
            ) : (
              <>
                {analyzedText && (
                  <><h3>Original Input</h3><pre className="output-raw-input">{analyzedText}</pre></>
                )}

                {summary && (
                  <>
                    <div className="analysis-header">
                      <h3>Cybersecurity Co-Pilot Analysis</h3>
                      {/* NEW: This is the severity badge */}
                      {severity && <span className={`severity-badge severity-${severity.toLowerCase()}`}>{severity}</span>}
                    </div>
                    <p className="output-summary">• {summary}</p>
                    {action && (
                      <><h3>Recommended Action</h3><pre className="output-action">{action}</pre></>
                    )}
                    {confidence && <p className="confidence">Confidence: {confidence}</p>}
                  </>
                )}
                {!summary && !isLoading && (
                  <p className="empty-output-message">
                    Paste some logs or messages and click "Analyze Text" to see the AI's interpretation.
                  </p>
                )}
              </>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;