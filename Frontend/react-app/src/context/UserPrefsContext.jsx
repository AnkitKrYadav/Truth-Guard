import React, { createContext, useContext, useState } from "react";

const UserPrefsContext = createContext();

export const UserPrefsProvider = ({ children }) => {
  const [userPrefs, setUserPrefs] = useState({
    preferredLanguage: "English",
    showConfidence: true,
  });

  const updatePrefs = (prefs) =>
    setUserPrefs((prev) => ({ ...prev, ...prefs }));

  return (
    <UserPrefsContext.Provider value={{ userPrefs, updatePrefs }}>
      {children}
    </UserPrefsContext.Provider>
  );
};

export const useUserPrefs = () => useContext(UserPrefsContext);
