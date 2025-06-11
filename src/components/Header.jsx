import { useApp } from "../context/AppContext";
import "./Header.css";

const Header = () => {
  const { searchQuery, dispatch, ACTIONS, mobileMenuOpen } = useApp();

  const handleSearch = (e) => {
    e.preventDefault();
    // Search is handled automatically by the context
  };

  const handleSearchChange = (e) => {
    dispatch({
      type: ACTIONS.SET_SEARCH_QUERY,
      payload: e.target.value,
    });
  };

  const handleCategoryClick = (category) => {
    dispatch({
      type: ACTIONS.SET_ACTIVE_CATEGORY,
      payload: category,
    });

    // Scroll to posts section
    const latestPostsSection = document.getElementById("latest-posts");
    if (latestPostsSection) {
      latestPostsSection.scrollIntoView({ behavior: "smooth" });
    }
  };

  const toggleMobileMenu = () => {
    dispatch({ type: ACTIONS.TOGGLE_MOBILE_MENU });
  };

  return (
    <header className="header">
      <div className="header-container">
        <div className="logo-section">
          <div className="logo-icon">📰</div>
          <h1 className="logo-text">Daily Post</h1>
        </div>

        <nav className={`navigation ${mobileMenuOpen ? "mobile-open" : ""}`}>
          <button
            onClick={() => handleCategoryClick("all")}
            className="nav-link active"
          >
            Home
          </button>
          <div className="categories-dropdown">
            <span className="nav-link">Categories ▼</span>
            <div className="dropdown-content">
              <button onClick={() => handleCategoryClick("sport")}>
                Sport
              </button>
              <button onClick={() => handleCategoryClick("politics")}>
                Politics
              </button>
              <button onClick={() => handleCategoryClick("news")}>News</button>
            </div>
          </div>
        </nav>

        <div className="search-section">
          <form onSubmit={handleSearch} className="search-form">
            <input
              type="text"
              placeholder="Search posts..."
              value={searchQuery}
              onChange={handleSearchChange}
              className="search-input"
            />
            <button type="submit" className="search-button">
              🔍
            </button>
          </form>
        </div>

        <div className="mobile-menu-toggle" onClick={toggleMobileMenu}>
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </header>
  );
};

export default Header;
