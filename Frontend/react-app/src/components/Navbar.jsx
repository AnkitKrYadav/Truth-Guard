import React from "react";
import { useTheme } from "../context/ThemeContext";
import { Moon, Sun } from "lucide-react";

function Navbar() {
  const { theme, toggleTheme } = useTheme();

  return (
    <nav className="flex items-center justify-between p-4 border-b dark:border-gray-700 bg-white dark:bg-gray-900">
      <h1 className="text-xl font-bold text-gray-800 dark:text-gray-100">
        TruthGuard
      </h1>

      <button
        onClick={toggleTheme}
        className="p-2 rounded-full bg-gray-200 dark:bg-gray-700 hover:opacity-80 transition"
      >
        {theme === "light" ? (
          <Moon size={18} className="text-gray-800" />
        ) : (
          <Sun size={18} className="text-yellow-400" />
        )}
      </button>
    </nav>
  );
}

export default Navbar;
