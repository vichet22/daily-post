import './Footer.css'

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-content">
          <div className="footer-section">
            <div className="footer-logo">
              <span className="footer-logo-icon">📰</span>
              <span className="footer-logo-text">Daily Post</span>
            </div>
            <p className="footer-description">
              Your trusted source for daily news, stories, and updates from around the world.
            </p>
          </div>

          <div className="footer-section">
            <h3 className="footer-title">Categories</h3>
            <ul className="footer-links">
              <li><a href="/sport">Sport</a></li>
              <li><a href="/politics">Politics</a></li>
              <li><a href="/news">News</a></li>
            </ul>
          </div>

          <div className="footer-section">
            <h3 className="footer-title">Quick Links</h3>
            <ul className="footer-links">
              <li><a href="/">Home</a></li>
              <li><a href="/about">About Us</a></li>
              <li><a href="/contact">Contact</a></li>
              <li><a href="/privacy">Privacy Policy</a></li>
            </ul>
          </div>

          <div className="footer-section">
            <h3 className="footer-title">Stay Updated</h3>
            <p className="newsletter-text">Subscribe to our newsletter for the latest updates</p>
            <div className="newsletter-form">
              <input 
                type="email" 
                placeholder="Enter your email"
                className="newsletter-input"
              />
              <button className="newsletter-btn">Subscribe</button>
            </div>
          </div>
        </div>

        <div className="footer-bottom">
          <p>&copy; 2025 Daily Post. All rights reserved.</p>
          <p>Built with React + Vite</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
