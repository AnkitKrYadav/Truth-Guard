import React, { useEffect, useState } from "react";
import StatsWidget from "../components/StatsWidget";
import NewsCard from "../components/NewsCard";
import VerificationItem from "../components/VerificationItem";
import axios from "axios";

const Dashboard = () => {
  const [trendingNews, setTrendingNews] = useState([]);
  const [verifications, setVerifications] = useState([]);
  const [stats, setStats] = useState([]);
  const [loading, setLoading] = useState(true);

  // Use env variable for API base; empty string defaults to same-origin
  const API_BASE = process.env.REACT_APP_API_BASE || "";

  useEffect(() => {
    async function fetchData() {
      try {
        // Fetch trending news
        const newsRes = await axios.get(`${API_BASE}/api/trending`);
        setTrendingNews(newsRes.data);

        // Fetch verifications (first 10 items)
        const verRes = await axios.get(`${API_BASE}/api/verifications?page=1&page_size=10`);
        setVerifications(verRes.data.items || []);

        // Build stats (currently using placeholders for "New Users" and "Fact Checks Completed")
        const statsData = [
          { title: "Verified Claims", value: verRes.data.items?.length || 0, icon: "✅", bgColor: "bg-green-100" },
          { title: "Trending Today", value: newsRes.data.length, icon: "🔥", bgColor: "bg-red-100" },
          { title: "New Users", value: 10, icon: "👤", bgColor: "bg-blue-100" }, // placeholder
          { title: "Fact Checks Completed", value: 180, icon: "📊", bgColor: "bg-yellow-100" } // placeholder
        ];
        setStats(statsData);

      } catch (err) {
        console.error("Error fetching dashboard data:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [API_BASE]);

  return (
    <div className="p-6 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 min-h-screen space-y-6">
      {/* Stats Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, idx) => (
          <StatsWidget key={idx} {...stat} />
        ))}
      </div>

      {/* Trending News Section */}
      <div>
        <h2 className="text-2xl font-bold mt-6 mb-4">Trending News</h2>
        {loading ? (
          <p>Loading news...</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {trendingNews.map((news) => (
              <NewsCard key={news.id} {...news} />
            ))}
          </div>
        )}
      </div>

      {/* Recent Verifications Section */}
      <div>
        <h2 className="text-2xl font-bold mt-6 mb-4">Recent Verifications</h2>
        {verifications.length === 0 ? (
          <p>No verifications yet.</p>
        ) : (
          <div className="grid grid-cols-1 gap-3">
            {verifications.map((v) => (
              <VerificationItem key={v.id} item={v} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
