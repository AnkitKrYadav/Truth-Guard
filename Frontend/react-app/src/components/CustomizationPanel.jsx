import React from "react";
import { useUserPrefs } from "../context/UserPrefsContext";

function CustomizationPanel() {
  const { userPrefs, updatePrefs } = useUserPrefs();

  return (
    <div className="bg-white dark:bg-gray-800 shadow-md rounded-lg p-4 space-y-4">
      <div>
        <label className="block text-gray-700 dark:text-gray-300 font-medium mb-1">
          Preferred Language
        </label>
        <select
          value={userPrefs.preferredLanguage}
          onChange={(e) => updatePrefs({ preferredLanguage: e.target.value })}
          className="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600"
        >
          <option>English</option>
          <option>Hindi</option>
          <option>Spanish</option>
          <option>French</option>
        </select>
      </div>

      <div>
        <label className="flex items-center gap-2 text-gray-700 dark:text-gray-300 font-medium">
          <input
            type="checkbox"
            checked={userPrefs.showConfidence}
            onChange={(e) => updatePrefs({ showConfidence: e.target.checked })}
            className="rounded"
          />
          Show confidence levels in results
        </label>
      </div>
    </div>
  );
}

export default CustomizationPanel;
