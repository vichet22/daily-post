import PostCard from "./PostCard";
import { useApp } from "../context/AppContext";
import { usePosts } from "../context/PostsContext";
import { categories } from "../data/posts";
import "./LatestPosts.css";

const LatestPosts = () => {
  const {
    activeCategory,
    searchQuery,
    dispatch,
    ACTIONS,
    currentPage,
    postsPerPage,
  } = useApp();

  const { posts } = usePosts();

  // Filter posts based on category and search
  const filteredPosts = posts.filter((post) => {
    const matchesCategory =
      activeCategory === "all" ||
      post.category.toLowerCase() === activeCategory;

    const matchesSearch =
      searchQuery === "" ||
      post.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      post.excerpt.toLowerCase().includes(searchQuery.toLowerCase()) ||
      post.content.toLowerCase().includes(searchQuery.toLowerCase());

    return matchesCategory && matchesSearch;
  });

  const paginatedPosts = filteredPosts.slice(0, currentPage * postsPerPage);
  const hasMorePosts = filteredPosts.length > paginatedPosts.length;

  return (
    <section id="latest-posts" className="latest-posts">
      <div className="latest-posts-container">
        <div className="section-header">
          <h2 className="section-title">
            {searchQuery
              ? `Search Results for "${searchQuery}"`
              : "Latest Posts"}
          </h2>
          <p className="section-description">
            {searchQuery
              ? `Found ${paginatedPosts.length} posts matching your search`
              : ""}
          </p>
        </div>

        <div className="category-filters">
          {categories.map((category) => (
            <button
              key={category.id}
              className={`category-filter ${
                activeCategory === category.id ? "active" : ""
              }`}
              onClick={() =>
                dispatch({
                  type: ACTIONS.SET_ACTIVE_CATEGORY,
                  payload: category.id,
                })
              }
              style={{
                "--category-color": category.color,
                backgroundColor:
                  activeCategory === category.id
                    ? category.color
                    : "transparent",
                color:
                  activeCategory === category.id ? "white" : category.color,
                borderColor: category.color,
              }}
            >
              {category.name}
            </button>
          ))}
        </div>

        <div className="posts-grid">
          {paginatedPosts.length > 0 ? (
            paginatedPosts.map((post) => <PostCard key={post.id} post={post} />)
          ) : (
            <div className="no-posts">
              <div className="no-posts-icon">📰</div>
              <h3>No posts found</h3>
              <p>
                {searchQuery
                  ? "Try adjusting your search terms or browse different categories."
                  : "Try selecting a different category to see more posts."}
              </p>
            </div>
          )}
        </div>

        {hasMorePosts && (
          <div className="load-more-section">
            <button
              className="load-more-button"
              onClick={() => {
                const currentPage = Math.floor(paginatedPosts.length / 6) + 1;
                dispatch({
                  type: ACTIONS.SET_CURRENT_PAGE,
                  payload: currentPage,
                });
              }}
            >
              Load More Posts
            </button>
          </div>
        )}
      </div>
    </section>
  );
};

export default LatestPosts;
