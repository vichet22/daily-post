import "./Hero.css";

const Hero = () => {
  const handleReadLatestPosts = () => {
    // Scroll to latest posts section
    const latestPostsSection = document.getElementById("latest-posts");
    if (latestPostsSection) {
      latestPostsSection.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <section className="hero">
      <div className="hero-container">
        <div className="hero-content">
          <h1 className="hero-title">Welcome to Daily Post</h1>
          <p className="hero-description">
            Stay informed with the latest news, stories, and updates from around
            the world. Your trusted source for daily information.
          </p>
          <button className="hero-cta-button" onClick={handleReadLatestPosts}>
            📖 Read Latest Posts
          </button>
        </div>

        <div className="hero-visual">
          <div className="hero-card">
            <div className="card-lines">
              <div className="line long"></div>
              <div className="line medium"></div>
              <div className="line short"></div>
              <div className="line medium"></div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
