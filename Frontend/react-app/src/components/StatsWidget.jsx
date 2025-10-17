import React from "react";

const StatsWidget = ({ title, value, icon, bgColor }) => (
  <div className={`flex items-center p-4 rounded-lg shadow-md ${bgColor}`}>
    <div className="text-3xl mr-4">{icon}</div>
    <div>
      <h3 className="text-gray-900 font-semibold">{title}</h3>
      <p className="text-xl font-bold text-gray-900">{value}</p>
    </div>
  </div>
);

export default StatsWidget;
