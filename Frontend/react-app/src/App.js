import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";

import Dashboard from "./pages/Dashboard";
import Verify from "./pages/Verify";
import Trending from "./pages/Trending";
import History from "./pages/History";
import Settings from "./pages/Settings";
import About from "./pages/About";

import { ThemeProvider } from "./context/ThemeContext";
import { UserPrefsProvider } from "./context/UserPrefsContext";
import "./index.css";

function App() {
  return (
    <ThemeProvider>
      <UserPrefsProvider>
        <Router>
          <div className="flex h-screen bg-gray-50 text-gray-900">
            <Sidebar />
            <div className="flex flex-col flex-grow">
              <Navbar />
              <main className="flex-grow overflow-y-auto p-6">
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/verify" element={<Verify />} />
                  <Route path="/trending" element={<Trending />} />
                  <Route path="/history" element={<History />} />
                  <Route path="/settings" element={<Settings />} />
                  <Route path="/about" element={<About />} />
                </Routes>
              </main>
            </div>
          </div>
        </Router>
      </UserPrefsProvider>
    </ThemeProvider>
  );
}

export default App;
