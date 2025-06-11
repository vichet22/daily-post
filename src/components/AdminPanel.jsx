import { useState } from "react";
import { useApp } from "../context/AppContext";
import { Link } from "react-router-dom";
import AdminLogin from "./AdminLogin";
import "./AdminPanel.css";

const AdminPanel = () => {
  const { posts, dispatch, ACTIONS, adminMode, adminAuthenticated } = useApp();
  const [showForm, setShowForm] = useState(false);
  const [editingPost, setEditingPost] = useState(null);
  const [showLogin, setShowLogin] = useState(false);
  const [formData, setFormData] = useState({
    title: "",
    excerpt: "",
    content: "",
    category: "NEWS",
    author: "Admin",
    image: "",
    readTime: "5 min read",
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!formData.title || !formData.excerpt || !formData.content) {
      alert("Please fill in all required fields");
      return;
    }

    if (editingPost) {
      dispatch({
        type: ACTIONS.UPDATE_POST,
        payload: { ...formData, id: editingPost.id },
      });
    } else {
      dispatch({
        type: ACTIONS.ADD_POST,
        payload: formData,
      });
    }

    resetForm();
  };

  const resetForm = () => {
    setFormData({
      title: "",
      excerpt: "",
      content: "",
      category: "NEWS",
      author: "Admin",
      image: "",
      readTime: "5 min read",
    });
    setEditingPost(null);
    setShowForm(false);
  };

  const handleEdit = (post) => {
    setFormData({
      title: post.title,
      excerpt: post.excerpt,
      content: post.content,
      category: post.category,
      author: post.author,
      image: post.image,
      readTime: post.readTime,
    });
    setEditingPost(post);
    setShowForm(true);
  };

  const handleDelete = (postId) => {
    if (window.confirm("Are you sure you want to delete this post?")) {
      dispatch({
        type: ACTIONS.DELETE_POST,
        payload: postId,
      });
    }
  };

  const toggleAdminMode = () => {
    if (!adminAuthenticated) {
      setShowLogin(true);
    } else {
      dispatch({
        type: ACTIONS.SET_ADMIN_MODE,
        payload: !adminMode,
      });
    }
  };

  const handleLogout = () => {
    if (window.confirm("Are you sure you want to logout from admin panel?")) {
      dispatch({ type: ACTIONS.ADMIN_LOGOUT });
      setShowForm(false);
      setEditingPost(null);
    }
  };

  if (!adminMode) {
    return (
      <>{showLogin && <AdminLogin onClose={() => setShowLogin(false)} />}</>
    );
  }

  return (
    <div className="admin-panel">
      <div className="admin-header">
        <div className="admin-title-section">
          <h2>Admin Panel</h2>
          <div className="admin-status">
            <span className="status-indicator">🟢</span>
            <span>Authenticated as Admin</span>
          </div>
        </div>
        <div className="admin-actions">
          <button
            onClick={() => setShowForm(!showForm)}
            className="add-post-button"
          >
            ➕ {showForm ? "Cancel" : "Add New Post"}
          </button>
          <button onClick={handleLogout} className="logout-button">
            🚪 Logout
          </button>
          <button onClick={toggleAdminMode} className="exit-admin-button">
            ✕ Exit Admin
          </button>
        </div>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="post-form">
          <h3>{editingPost ? "Edit Post" : "Create New Post"}</h3>

          <div className="form-group">
            <label htmlFor="title">Title *</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="category">Category</label>
              <select
                id="category"
                name="category"
                value={formData.category}
                onChange={handleInputChange}
              >
                <option value="NEWS">News</option>
                <option value="SPORT">Sport</option>
                <option value="POLITICS">Politics</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="author">Author</label>
              <input
                type="text"
                id="author"
                name="author"
                value={formData.author}
                onChange={handleInputChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="readTime">Read Time</label>
              <input
                type="text"
                id="readTime"
                name="readTime"
                value={formData.readTime}
                onChange={handleInputChange}
                placeholder="5 min read"
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="image">Image URL</label>
            <input
              type="url"
              id="image"
              name="image"
              value={formData.image}
              onChange={handleInputChange}
              placeholder="https://example.com/image.jpg"
            />
          </div>

          <div className="form-group">
            <label htmlFor="excerpt">Excerpt *</label>
            <textarea
              id="excerpt"
              name="excerpt"
              value={formData.excerpt}
              onChange={handleInputChange}
              rows="3"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="content">Content *</label>
            <textarea
              id="content"
              name="content"
              value={formData.content}
              onChange={handleInputChange}
              rows="6"
              required
            />
          </div>

          <div className="form-actions">
            <button type="submit" className="submit-button">
              {editingPost ? "Update Post" : "Create Post"}
            </button>
            <button type="button" onClick={resetForm} className="cancel-button">
              Cancel
            </button>
          </div>
        </form>
      )}

      <div className="posts-management">
        <h3>Manage Posts ({posts.length})</h3>
        <div className="posts-list">
          {posts.map((post) => (
            <div key={post.id} className="post-item">
              <div className="post-info">
                <h4>{post.title}</h4>
                <p>
                  {post.category} • {post.author} • {post.date}
                </p>
              </div>
              <div className="post-actions">
                <button
                  onClick={() => handleEdit(post)}
                  className="edit-button"
                >
                  ✏️ Edit
                </button>
                <button
                  onClick={() => handleDelete(post.id)}
                  className="delete-button"
                >
                  🗑️ Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {showLogin && <AdminLogin onClose={() => setShowLogin(false)} />}
    </div>
  );
};

export default AdminPanel;
