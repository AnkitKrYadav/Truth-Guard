import React, { useEffect, useState } from "react";
import StatsWidget from "../components/StatsWidget";
import NewsCard from "../components/NewsCard";
import client from "../utils/api";

const Trending = () => {
  const [trendingNews, setTrendingNews] = useState([]);
  const [categories, setCategories] = useState(["All"]);
  const [filter, setFilter] = useState("All");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const newsRes = await client.get(`/api/trending`);
        setTrendingNews(newsRes.data);

        const catRes = await client.get(`/api/categories`);
        setCategories(catRes.data);
      } catch (err) {
        console.error("Error fetching trending:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  const filteredNews = trendingNews.filter(
    (item) => filter === "All" || item.category === filter
  );

  return (
    <div className="p-6 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 min-h-screen space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Trending Topics</h1>

      <div className="flex gap-4 overflow-x-auto py-4">
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setFilter(cat)}
            className={`px-4 py-2 rounded-full font-medium transition ${
              filter === cat
                ? "bg-blue-600 text-white"
                : "bg-gray-200 text-gray-700 hover:bg-blue-500 hover:text-white"
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {loading ? (
        <p>Loading trending news...</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredNews.map((news) => (
            <NewsCard key={news.id} {...news} />
          ))}
        </div>
      )}
    </div>
  );
};

export default Trending;
