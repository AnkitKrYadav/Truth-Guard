import React from "react";
import { Moon, Sun } from "lucide-react";
import { useTheme } from "../context/ThemeContext";

function Navbar() {
  const { theme, toggleTheme } = useTheme();

  return (
    <nav className="flex justify-between items-center bg-white/70 backdrop-blur-md px-6 py-3 shadow-sm sticky top-0 z-40">
      <h1 className="text-xl font-semibold">TruthGuard Dashboard</h1>
      <button
        onClick={toggleTheme}
        className="p-2 rounded-lg hover:bg-gray-200 transition"
      >
        {theme === "light" ? (
          <Moon className="w-5 h-5 text-gray-700" />
        ) : (
          <Sun className="w-5 h-5 text-yellow-400" />
        )}
      </button>
    </nav>
  );
}

export default Navbar;
