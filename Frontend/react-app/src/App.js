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
        <Router basename={process.env.PUBLIC_URL}>
          <div className="p-6 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 min-h-screen flex h-screen">
            <Sidebar />
            <div className="flex flex-col flex-grow">
              <Navbar />
              <main className="flex-grow overflow-y-auto">
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
