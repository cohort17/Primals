import React, { useState } from "react";
import { TOKEN_ID } from "./config";
import "./App.css";

function App() {
  const [address, setAddress] = useState("");
  const [balance, setBalance] = useState(null);

  // Simulate backend call
  const getBalance = async () => {
    // Replace this with actual API call to your backend
    // For now, just fake a response
    setBalance("1000 PRIMALS");
  };

  return (
    <div className="App">
      <header>
        <h1>Primals Wallet</h1>
        <p>
          Token ID: <code>{TOKEN_ID}</code>
        </p>
      </header>
      <main>
        <div>
          <input
            type="text"
            placeholder="Enter your address"
            value={address}
            onChange={e => setAddress(e.target.value)}
          />
          <button onClick={getBalance}>Check Balance</button>
        </div>
        {balance && (
          <div>
            <p>
              Balance for <b>{address}</b>: <span>{balance}</span>
            </p>
          </div>
        )}
      </main>
      <footer>
        <p>&copy; {new Date().getFullYear()} Primals Project</p>
      </footer>
    </div>
  );
}

export default App;
