import React from "react";
import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  ShieldCheck,
  TrendingUp,
  History,
  Settings,
  Info,
} from "lucide-react";

const links = [
  { to: "/", icon: LayoutDashboard, label: "Dashboard" },
  { to: "/verify", icon: ShieldCheck, label: "Verify" },
  { to: "/trending", icon: TrendingUp, label: "Trending" },
  { to: "/history", icon: History, label: "History" },
  { to: "/settings", icon: Settings, label: "Settings" },
  { to: "/about", icon: Info, label: "About" },
];

function Sidebar() {
  return (
    <aside className="hidden md:flex flex-col w-64 bg-white border-r shadow-sm">
      <div className="p-5 border-b">
        <h2 className="text-2xl font-bold text-blue-600">TruthGuard</h2>
      </div>
      <nav className="flex-grow px-4 py-6 space-y-2">
        {links.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2 rounded-lg font-medium transition-all duration-150 ${
                isActive
                  ? "bg-blue-600 text-white shadow"
                  : "text-gray-700 hover:bg-blue-50"
              }`
            }
          >
            <Icon className="w-5 h-5" />
            {label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}

export default Sidebar;
