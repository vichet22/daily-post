import { useApp } from "../context/AppContext";
import "./PostCard.css";

const PostCard = ({ post }) => {
  const { dispatch, ACTIONS } = useApp();

  const getCategoryColor = (category) => {
    const colors = {
      SPORT: "#ff9500",
      NEWS: "#34c759",
      POLITICS: "#007aff",
    };
    return colors[category] || "#4285f4";
  };

  const handleReadMore = () => {
    dispatch({
      type: ACTIONS.SET_SELECTED_POST,
      payload: post,
    });
  };

  return (
    <article className="post-card">
      <div className="post-image-container">
        <img
          src={post.image}
          alt={post.title}
          className="post-image"
          loading="lazy"
        />
        <div
          className="post-category-badge"
          style={{ backgroundColor: getCategoryColor(post.category) }}
        >
          {post.category}
        </div>
      </div>

      <div className="post-content">
        <div className="post-meta">
          <span className="post-date">{post.date}</span>
          <span className="post-read-time">{post.readTime}</span>
        </div>

        <h3 className="post-title">{post.title}</h3>

        <p className="post-excerpt">{post.excerpt}</p>

        <div className="post-footer">
          <div className="post-author">
            <div className="author-avatar">👤</div>
            <span className="author-name">By {post.author}</span>
          </div>

          <button
            className="read-more-button"
            onClick={handleReadMore}
            style={{ backgroundColor: getCategoryColor(post.category) }}
          >
            Read Full Article →
          </button>
        </div>
      </div>
    </article>
  );
};

export default PostCard;
