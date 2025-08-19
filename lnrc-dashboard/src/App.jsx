import React from "react";
import LNRCStats from "./components/LNRCStats";

function App() {
  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <header className="text-center mb-8">
        <h1 className="text-4xl font-bold">👑 Le Noble Roi Chat (LNRC)</h1>
        <p className="text-sm text-gray-400">
          Dashboard en temps réel – rotation, burn, prix LNRC
        </p>
      </header>

      <main className="max-w-3xl mx-auto">
        <LNRCStats />
      </main>

      <footer className="mt-10 text-center text-gray-600 text-xs">
        &copy; 2025 LNRC – Propulsé par Web3 et BscScan
      </footer>
    </div>
  );
}

export default App;
