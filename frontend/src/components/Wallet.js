import React, { useState } from "react";
import axios from "axios";
import { isValidAddress, isValidAmount } from "../utils/validation";

export default function Wallet({ tokenId }) {
    const [balance, setBalance] = useState(null);
    const [address, setAddress] = useState("");
    const [amount, setAmount] = useState("");
    const [error, setError] = useState("");

    const getBalance = async () => {
        try {
            const res = await axios.get(`/api/balance?tokenid=${tokenId}`);
            setBalance(res.data.balance);
            setError("");
        } catch (e) {
            setError("Could not fetch balance.");
        }
    };

    const sendToken = async () => {
        if (!isValidAddress(address)) {
            setError("Invalid recipient address.");
            return;
        }
        if (!isValidAmount(amount)) {
            setError("Invalid amount.");
            return;
        }
        try {
            await axios.post("/api/send", { address, amount, tokenid: tokenId });
            setError("");
            getBalance();
        } catch (e) {
            setError("Transaction failed.");
        }
    };

    return (
        <div>
            <h2>Minima Wallet</h2>
            {error && <div style={{ color: "red" }}>{error}</div>}
            <button onClick={getBalance}>Check Balance</button>
            <div>Balance: {balance}</div>
            <input
                placeholder="Recipient Address"
                value={address}
                onChange={e => setAddress(e.target.value)}
            />
            <input
                placeholder="Amount"
                value={amount}
                onChange={e => setAmount(e.target.value)}
            />
            <button onClick={sendToken}>Send</button>
        </div>
    );
}
