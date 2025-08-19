import React, { useEffect, useState } from "react";
import axios from "axios";

const LNRCStats = () => {
  const [balances, setBalances] = useState([]);
  const [price, setPrice] = useState(null);

  const API_KEY = import.meta.env.VITE_BSCSCAN_API_KEY;
  const CONTRACT_ADDRESS = "0xc78056f834ad22356051af603f2e89c8398838f5";
  const WALLETS = [
    import.meta.env.VITE_WALLET_1,
    import.meta.env.VITE_WALLET_2,
    import.meta.env.VITE_WALLET_3,
    import.meta.env.VITE_WALLET_4
  ];

  const getBalance = async (wallet) => {
    try {
      const res = await axios.get(
        `https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=${CONTRACT_ADDRESS}&address=${wallet}&tag=latest&apikey=${API_KEY}`
      );
      return {
        wallet,
        balance: parseFloat(res.data.result) / 1e18
      };
    } catch (err) {
      return { wallet, balance: 0 };
    }
  };

  const fetchBalances = async () => {
    const results = await Promise.all(WALLETS.map(getBalance));
    setBalances(results);
  };

  const fetchPrice = async () => {
    try {
      const res = await axios.get(
        `https://api.coingecko.com/api/v3/simple/token_price/binance-smart-chain?contract_addresses=${CONTRACT_ADDRESS}&vs_currencies=usd`
      );
      setPrice(res.data[CONTRACT_ADDRESS.toLowerCase()]?.usd || "N/A");
    } catch (err) {
      setPrice("N/A");
    }
  };

  useEffect(() => {
    fetchBalances();
    fetchPrice();
  }, []);

  return (
    <div className="p-4 bg-white rounded-2xl shadow-md max-w-xl mx-auto">
      <h2 className="text-xl font-bold mb-4">Statistiques LNRC</h2>
      <p className="mb-4">💰 Prix LNRC : <strong>{price} $</strong></p>
      <h3 className="font-semibold">📦 Balances des wallets :</h3>
      <ul className="list-disc list-inside">
        {balances.map((b, index) => (
          <li key={index}>
            Wallet {index + 1} : {b.balance.toFixed(2)} LNRC
          </li>
        ))}
      </ul>
    </div>
  );
};

export default LNRCStats;
