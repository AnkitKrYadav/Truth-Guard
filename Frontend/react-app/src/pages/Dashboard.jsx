import React, { useEffect, useState } from "react";
import StatsWidget from "../components/StatsWidget";
import NewsCard from "../components/NewsCard";
import VerificationItem from "../components/VerificationItem";
import client from "../utils/api";

const Dashboard = () => {
  const [trendingNews, setTrendingNews] = useState([]);
  const [verifications, setVerifications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const newsRes = await client.get("/api/trending");
        setTrendingNews(newsRes.data);

        const verRes = await client.get("/api/verifications?page=1&page_size=10");
        setVerifications(verRes.data.items || []);
      } catch (err) {
        console.error("Dashboard fetch error:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  const statsData = [
    { title: "Verified Claims", value: verifications.length, icon: "✅", bgColor: "bg-green-100" },
    { title: "Trending Today", value: trendingNews.length, icon: "🔥", bgColor: "bg-red-100" },
    { title: "New Users", value: 320, icon: "👤", bgColor: "bg-blue-100" },
    { title: "Fact Checks Completed", value: verifications.length, icon: "📊", bgColor: "bg-yellow-100" }
  ];

  return (
    <div className="p-6 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 min-h-screen space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {statsData.map((stat, idx) => (
          <StatsWidget key={idx} {...stat} />
        ))}
      </div>

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
