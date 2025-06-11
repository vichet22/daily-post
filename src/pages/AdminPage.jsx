import { useState, useEffect } from "react";
import { useApp } from "../context/AppContext";
import AdminLogin from "../components/AdminLogin";
import "./AdminPage.css";

const AdminPage = () => {
  const { posts, dispatch, ACTIONS, adminAuthenticated } = useApp();

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
    imageFile: null,
    readTime: "5 min read",
  });

  // Check authentication on page load
  useEffect(() => {
    if (!adminAuthenticated) {
      setShowLogin(true);
    }
  }, [adminAuthenticated]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Create a preview URL for the uploaded file
      const imageUrl = URL.createObjectURL(file);
      setFormData((prev) => ({
        ...prev,
        imageFile: file,
        image: imageUrl,
      }));
    }
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
      imageFile: null,
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
      imageFile: null,
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

  const handleLogout = () => {
    if (window.confirm("Are you sure you want to logout from admin panel?")) {
      dispatch({ type: ACTIONS.ADMIN_LOGOUT });
      setShowForm(false);
      setEditingPost(null);
      setShowLogin(true);
    }
  };

  const goToHomePage = () => {
    window.location.href = "/";
  };

  // Show login if not authenticated
  if (!adminAuthenticated) {
    return (
      <div className="admin-page">
        <div className="admin-page-header">
          <div className="admin-page-nav">
            <button onClick={goToHomePage} className="home-button">
              🏠 Back to Home
            </button>
            <h1>Daily Post Admin</h1>
          </div>
        </div>

        <div className="admin-login-container">
          <div className="login-welcome">
            <h2>Welcome to Admin Panel</h2>
            <p>Please login to access the admin dashboard</p>
          </div>
        </div>

        {showLogin && <AdminLogin onClose={() => setShowLogin(false)} />}
      </div>
    );
  }

  return (
    <div className="admin-page">
      <div className="admin-page-header">
        <div className="admin-page-nav">
          <button onClick={goToHomePage} className="home-button">
            🏠 Back to Home
          </button>
          <div className="admin-title-section">
            <h1>Daily Post Admin</h1>
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
          </div>
        </div>
      </div>

      <div className="admin-content">
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

            <div className="image-section">
              <h4 className="section-title">Post Image (Optional)</h4>
              <p className="section-description">
                Choose either an image URL or upload a file. File upload will
                override URL.
              </p>

              <div className="form-row">
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
                  <label htmlFor="imageFile">Upload Image File</label>
                  <input
                    type="file"
                    id="imageFile"
                    name="imageFile"
                    onChange={handleFileChange}
                    accept="image/*"
                    className="file-input"
                  />
                  {formData.imageFile && (
                    <div className="file-preview">
                      <span className="file-name">
                        📁 {formData.imageFile.name}
                      </span>
                    </div>
                  )}
                </div>
              </div>
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
              <button
                type="button"
                onClick={resetForm}
                className="cancel-button"
              >
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
      </div>
    </div>
  );
};

export default AdminPage;
